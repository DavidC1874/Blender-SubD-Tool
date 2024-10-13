bl_info = {
    "name":"SubD Adder",
    "author":"David Cai",
    "version":(1,0),
    "blender":(2,90,0),
    "location":"View 3D > Tool Shelf",
    "category":"Tool",
}




import bpy
from bpy.props import IntProperty

class SubdAddOperator(bpy.types.Operator):
    bl_idname = "subd.add_operator"
    bl_label = "Add Subdivision"
    
    level: IntProperty(
        name="Viewport Level",
        description="SubD View",
        default=2,
        min=0,
        max=4
    )
    
    render_level: IntProperty(
        name="Render Level",
        description="SubD Render",
        default=3,
        min=0,
        max=6
    )

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                if "Subdivision" not in obj.modifiers:
                    modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
                    modifier.levels = self.level
                    modifier.render_levels = self.render_level
        return {'FINISHED'}


class SubdAddPopup(bpy.types.Operator):
    bl_idname = "subd.add_popup"
    bl_label = "Add Subdivision Levels"
    bl_options = {'REGISTER', 'UNDO'}

    level: IntProperty(
        name="Viewport Level",
        description="SubD View",
        default=2,
        min=0,
        max=4
    )
    
    render_level: IntProperty(
        name="Render Level",
        description="SubD Render",
        default=3,
        min=0,
        max=6
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "level")
        layout.prop(self, "render_level")

    def execute(self, context):
        bpy.ops.subd.add_operator(level=self.level, render_level=self.render_level)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class MainPanel(bpy.types.Panel):
    bl_label = "Subdivision Tool"
    bl_idname = "SUBD_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout 
        selected_objects = bpy.context.selected_objects

        if not selected_objects:
            layout.label(text="No object selected")
            return

        mesh_objects = [obj for obj in selected_objects if obj.type == 'MESH']

        if not mesh_objects:
            layout.label(text="No mesh objects selected")
            return

        no_subd_objects = [obj for obj in mesh_objects if "Subdivision" not in obj.modifiers]
        
        if no_subd_objects:
            layout.operator("subd.add_popup", text="Add Subdivision to Selected")
        else:
            layout.label(text="Adjust Subdivision for selected objects")
            for obj in mesh_objects:
                modifier = obj.modifiers.get("Subdivision")
                if modifier:
                    box = layout.box()
                    box.label(text=f"{obj.name} Subdivision")
                    box.prop(modifier, "levels", text="Viewport Levels")
                    box.prop(modifier, "render_levels", text="Render Levels")
                    
        row = layout.row()
        row.operator("delete.operator")
                    

class DelSubD(bpy.types.Operator):
    bl_idname = "delete.operator"
    bl_label = "Clear Subd"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        
        for obj in selected_objects:
            if obj.type == 'MESH':
                modifier = obj.modifiers.get("Subdivision")
                if modifier:
                    obj.modifiers.remove(modifier)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SubdAddOperator)
    bpy.utils.register_class(SubdAddPopup)
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(DelSubD)

def unregister():
    bpy.utils.unregister_class(SubdAddOperator)
    bpy.utils.unregister_class(SubdAddPopup)
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(DelSubD)

if __name__ == "__main__":
    register()
