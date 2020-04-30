import os,sys

# add folder containing FreeCAD.pyd, FreeCADGui.pyd to sys.path
sys.path.append("/usr/lib/freecad/lib") # example for Linux

import hashlib

from fabric.api import local, lcd

import FreeCAD
import FreeCADGui
import Mesh
import Part

def convert_stl_to_step(in_stl, out_step):
  print('converting stl to step: {} -> {}'.format(in_stl, out_step))
  in_stl = copy_stl_to_tmp_stl(in_stl)

  if os.path.exists(out_step):
      print('output step file exist, skipping ...')
      return

  try:

    print('converting ... ')
    Mesh.insert(in_stl)
    App.ActiveDocument.recompute()
    FreeCAD.getDocument("Unnamed").addObject("Part::Feature","test001")
    __shape__=Part.Shape()
    __shape__.makeShapeFromMesh(FreeCAD.getDocument("Unnamed").getObject("test").Mesh.Topology,0.100000)
    FreeCAD.getDocument("Unnamed").getObject("test001").Shape=__shape__
    FreeCAD.getDocument("Unnamed").getObject("test001").purgeTouched()
    del __shape__
    App.ActiveDocument.addObject('Part::Feature','test001').Shape=App.ActiveDocument.test001.Shape.removeSplitter()
    App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.test001.Label
    App.ActiveDocument.recompute()

    __objs__=[]
    __objs__.append(FreeCAD.getDocument("Unnamed").getObject("test001001"))
    Part.export(__objs__,out_step)
    del __objs__
  except:
    print("error during converting {}".format(in_stl))

  local('rm -rf "{}"'.format(os.path.dirname(in_stl)))

def get_temp_directory():
  return local('mktemp -d', capture=True)

def get_temp_stl_filename(in_stl):
  hex_digest = hashlib.md5(in_stl.encode()).hexdigest()
  return '{}/{}.stl'.format(get_temp_directory() , 'test')

def make_temp_stl_file(in_stl):
  temp_filename=get_temp_stl_filename(in_stl)
  return temp_filename

def copy_stl_to_tmp_stl(in_stl):
  stl_file_in_tmp_directory = make_temp_stl_file(in_stl)
  local('cp "{}" "{}"'.format(in_stl, stl_file_in_tmp_directory))
  return stl_file_in_tmp_directory

if __name__ == "__main__":
  convert_stl_to_step(sys.argv[1], sys.argv[2])