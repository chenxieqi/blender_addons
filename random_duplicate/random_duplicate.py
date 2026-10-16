# 選択されたオブジェクトをランダムの値で複製するBlenderアドオン
# サイズ（ｘ・ｙ・ｚ）、ローテーション（ｘ・ｙ・ｚ）、数を変更可能
bl_info = {
    "name": "Random Duplicate",
    "author": "chen xieqi",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Object > Duplicate",
    "description": "Randomly duplicate selected objects",
    "category": "Object",
}

import math
import random

import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty, PointerProperty
from mathutils import Euler, Quaternion



# ------------------------------------------------------------
#  設定
# ------------------------------------------------------------

class RDUPJA_Settings(bpy.types.PropertyGroup):

    # 基本
    count: IntProperty(
        name="複製する数",
        default=1,
        min=1,
        max=1000,
    )

    linked: BoolProperty(
        name="リンク複製",
        description="メッシュを共有します（Alt+D と同じ）",
        default=False,
    )


    # 大きさ
    use_scale: BoolProperty(
        name="大きさをランダムに",
        default=True,
    )

    scale_uniform: BoolProperty(
        name="縦横比を保つ",
        description="XYZ に同じ倍率を使います",
        default=True,
    )

    scale_relative: BoolProperty(
        name="元の大きさに掛ける",
        description="オフにすると、値をそのまま設定します",
        default=True,
    )

    scale_min: FloatProperty(name="最小", default=0.8, min=0.0, soft_max=10.0)
    scale_max: FloatProperty(name="最大", default=1.2, min=0.0, soft_max=10.0)


    # 回転
    use_rot_x: BoolProperty(name="X", default=False)
    use_rot_y: BoolProperty(name="Y", default=False)
    use_rot_z: BoolProperty(name="Z", default=True)

    rot_relative: BoolProperty(
        name="元の回転に足す",
        description="オフにすると、角度をそのまま設定します",
        default=True,
    )

    rot_x_min: FloatProperty(name="X 最小", default=-180.0, soft_min=-360.0, soft_max=360.0)
    rot_x_max: FloatProperty(name="X 最大", default=180.0, soft_min=-360.0, soft_max=360.0)

    rot_y_min: FloatProperty(name="Y 最小", default=-180.0, soft_min=-360.0, soft_max=360.0)
    rot_y_max: FloatProperty(name="Y 最大", default=180.0, soft_min=-360.0, soft_max=360.0)

    rot_z_min: FloatProperty(name="Z 最小", default=-180.0, soft_min=-360.0, soft_max=360.0)
    rot_z_max: FloatProperty(name="Z 最大", default=180.0, soft_min=-360.0, soft_max=360.0)


    # シード
    use_seed: BoolProperty(
        name="シードを固定",
        description="毎回同じ結果になります",
        default=False,
    )

    seed: IntProperty(name="シード", default=0, min=0)



# ------------------------------------------------------------
#  小さな関数
# ------------------------------------------------------------

def _rand(lo, hi):
    # 最小と最大が逆なら入れ替える
    if lo > hi:
        lo, hi = hi, lo

    return random.uniform(lo, hi)



def _duplicate(obj, linked):
    new = obj.copy()

    # リンク複製でなければ、メッシュも別にする
    if obj.data is not None and not linked:
        new.data = obj.data.copy()

    # アニメーションも別にする
    if obj.animation_data and obj.animation_data.action and not linked:
        new.animation_data.action = obj.animation_data.action.copy()

    # 元と同じコレクションに入れる
    for coll in obj.users_collection:
        coll.objects.link(new)

    return new



def _apply_scale(obj, s):

    if s.scale_uniform:
        f = _rand(s.scale_min, s.scale_max)
        factors = (f, f, f)
    else:
        factors = tuple(_rand(s.scale_min, s.scale_max) for _ in range(3))

    if s.scale_relative:
        obj.scale = tuple(obj.scale[i] * factors[i] for i in range(3))
    else:
        obj.scale = factors



def _apply_rotation(obj, s):

    axes = (
        (s.use_rot_x, s.rot_x_min, s.rot_x_max),
        (s.use_rot_y, s.rot_y_min, s.rot_y_max),
        (s.use_rot_z, s.rot_z_min, s.rot_z_max),
    )

    # どの軸もオフなら何もしない
    if not any(a[0] for a in axes):
        return


    # いったんオイラー角にする
    mode = obj.rotation_mode

    if mode == 'QUATERNION':
        euler = obj.rotation_quaternion.to_euler('XYZ')
    elif mode == 'AXIS_ANGLE':
        aa = obj.rotation_axis_angle
        euler = Quaternion(aa[1:], aa[0]).to_euler('XYZ')
    else:
        euler = obj.rotation_euler.copy()


    # 軸ごとにランダムな角度を入れる
    for i, (enabled, lo, hi) in enumerate(axes):
        if not enabled:
            continue

        angle = math.radians(_rand(lo, hi))
        euler[i] = euler[i] + angle if s.rot_relative else angle


    # 元の回転モードに戻す
    if mode == 'QUATERNION':
        obj.rotation_quaternion = euler.to_quaternion()
    elif mode == 'AXIS_ANGLE':
        axis, angle = euler.to_quaternion().to_axis_angle()
        obj.rotation_axis_angle = (angle, *axis)
    else:
        obj.rotation_euler = Euler(euler, mode)



# ------------------------------------------------------------
#  オペレーター
# ------------------------------------------------------------

class RDUPJA_OT_random_duplicate(bpy.types.Operator):
    bl_idname = "object.random_duplicate_ja"
    bl_label = "ランダム複製"
    bl_description = "選択したオブジェクトを複製し、大きさと回転をランダムに変えます"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects


    def execute(self, context):
        s = context.scene.rdupja_settings

        if s.use_seed:
            random.seed(s.seed)
        else:
            random.seed()


        # 複製する
        originals = list(context.selected_objects)
        new_objs = []

        for obj in originals:
            for _ in range(s.count):
                new = _duplicate(obj, s.linked)

                if s.use_scale:
                    _apply_scale(new, s)

                _apply_rotation(new, s)
                new_objs.append(new)


        # 選択を複製の方に移す
        for obj in originals:
            obj.select_set(False)

        for obj in new_objs:
            obj.select_set(True)

        if new_objs:
            context.view_layer.objects.active = new_objs[-1]


        self.report({'INFO'}, f"{len(new_objs)} 個 複製しました")
        return {'FINISHED'}



# ------------------------------------------------------------
#  パネル
# ------------------------------------------------------------

class RDUPJA_PT_panel(bpy.types.Panel):
    bl_label = "ランダム複製"
    bl_idname = "RDUPJA_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ランダム複製"


    def draw(self, context):
        s = context.scene.rdupja_settings
        layout = self.layout


        # 基本
        col = layout.column()
        col.prop(s, "count")
        col.prop(s, "linked")

        layout.separator()


        # 大きさ
        box = layout.box()
        box.prop(s, "use_scale")

        sub = box.column()
        sub.enabled = s.use_scale

        row = sub.row(align=True)
        row.prop(s, "scale_min")
        row.prop(s, "scale_max")

        sub.separator()
        sub.prop(s, "scale_uniform")
        sub.prop(s, "scale_relative")

        layout.separator()


        # 回転
        box = layout.box()
        box.label(text="回転（度）")

        for axis in ("x", "y", "z"):
            row = box.row(align=True)
            row.prop(s, f"use_rot_{axis}")

            r = row.row(align=True)
            r.enabled = getattr(s, f"use_rot_{axis}")
            r.prop(s, f"rot_{axis}_min", text="")
            r.prop(s, f"rot_{axis}_max", text="")

        box.separator()
        box.prop(s, "rot_relative")

        layout.separator()


        # シード
        row = layout.row(align=True)
        row.prop(s, "use_seed")

        r = row.row(align=True)
        r.enabled = s.use_seed
        r.prop(s, "seed")


        # 実行ボタン
        layout.separator(factor=2.0)
        layout.operator(
            RDUPJA_OT_random_duplicate.bl_idname,
            icon='DUPLICATE',
        )



# ------------------------------------------------------------
#  登録
# ------------------------------------------------------------

classes = (
    RDUPJA_Settings,
    RDUPJA_OT_random_duplicate,
    RDUPJA_PT_panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.rdupja_settings = PointerProperty(type=RDUPJA_Settings)


def unregister():
    del bpy.types.Scene.rdupja_settings

    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
