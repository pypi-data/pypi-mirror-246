# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    Methods for managing drawio drawings.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 15:45:00
    `memberOf`: drawio
    `name`: drawing
'''


from lxml import etree
from colemen_config import _diagram_type,_drawing_type,_Iterable,_Union
# import json as _json

import colemen_utilities.file_utils as _f
import colemen_utilities.dict_utils as _obj




from colemen_utilities.drawio.NodeBase import NodeBase as _NodeBase
from colemen_utilities.drawio.Diagram import new_diagram as _new_diagram
from colemen_utilities.drawio.Diagram import Diagram as _Diagram
# from diagram import new_diagram,Diagram



def new_drawing(**kwargs)->_drawing_type:
    '''
        Creates a new draw.io drawing.

        ----------

        Keyword Arguments
        -------------------------
        [`file_path`=None] {string}
            The path to where the drawing should be saved.

        Return {Drawing}
        ----------------------
        An instance of the Drawing class

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:22:38
        `memberOf`: drawing
        `version`: 1.0
        `method_name`: new_drawing
    '''

    file_path = _obj.get_kwarg(['file_path','path'],None,(str),**kwargs)

    mxfile = etree.Element("mxfile")
    mxfile.attrib['host'] = "Electron"
    mxfile.attrib['modified'] = "2022-05-26T18:37:31.077Z"
    mxfile.attrib['agent'] = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/14.9.6 Chrome/89.0.4389.128 Electron/12.0.16 Safari/537.36"
    mxfile.attrib['etag'] = "AdGKFnLcEHsRAx8fGjjM"
    mxfile.attrib['compressed'] = "false"
    mxfile.attrib['version'] = "14.9.6"
    mxfile.attrib['type'] = "device"
    dwg = Drawing(mxfile)
    if file_path is not None:
        dwg.set_file_path(file_path)
    return dwg

def read(file_path:str)->_drawing_type:
    '''
        Read an existing draw.io diagram.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The file_path to the diagram.

        Return {Drawing}
        ----------------------
        An instance of the Drawing class

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:31:54
        `memberOf`: drawing
        `version`: 1.0
        `method_name`: read
    '''


    xml = _f.readr(file_path)
    # tree = etree.parse(xml)
    tree = etree.fromstring(xml)
    drawing = Drawing(tree)
    drawing.data['file'] = _f.get_data(file_path)
    return drawing

class Drawing(_NodeBase):
    def __init__(self,tree,element=None):
        super().__init__(tree,element)
        self.settings = {}
        self.tree = tree
        self.element = element
        self.dia_root = None
        self.data = {
            "file":{
                "file_path":None,
            },
            "diagrams":[],
        }

        _get_diagrams(self)

    def new_diagram(self,name):
        '''
            Create a new diagram in the drawing.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the diagram, this is shown on tabs in draw.io

            Return {Diagram}
            ----------------------
            An instance of the Diagram class.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:34:35
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: new_diagram
        '''

        dia = _new_diagram(self.tree,name)
        self.data['diagrams'].append(dia)
        return dia



    def save(self,path=None):
        '''
            Save this drawing

            You should use set_file_path to set the default file_path for the drawing.

            ----------

            Arguments
            -------------------------
            [`path`=None] {str}
                Where to save this drawing, if not provided the default path will be used.

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                    arg_description

            Return {bool}
            ----------------------
            If no path is provided and there is no default path, it will return False.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:38:44
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: save
        '''


        # self.to_element()
        if path is None:
            if 'file_path' in self.data['file']:
                if self.data['file']['file_path'] is not None:
                    path = self.data['file']
            if path is None:
                return False
        _f.write(path,etree.tostring(self.tree).decode("utf-8"))
        return True

    def list_diagrams(self):
        '''
            list all diagrams that belong to this drawing.

            ----------

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:40:32
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: list_diagrams
        '''


        for d in self.data['diagrams']:
            if d.has_name():
                print(d.data['attributes']['name'])

    def get_diagram(self,name:str)->_Union[_diagram_type,None]:
        '''
            Get a diagram by its name.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the diagram to return.

            Return {Diagram}
            ----------------------
            The Diagram class instance with a matching name.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:41:56
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: get_diagram
        '''
        diagram:_diagram_type
        for diagram in self.data['diagrams']:
            if diagram.get_name(name):
                return diagram
        return None

    def set_file_path(self,value):
        '''
            Set the file_path for this drawing.

            ----------

            Arguments
            -------------------------
            `value` {str}
                The file_path to where this drawing will be saved.

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 12:30:13
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: set_file_path
        '''

        self.data['file']['file_path'] = value

    def get_file_path(self,test_value=None,default_val=None):
        '''
            Get the file_path attribute of the drawing.

            ----------

            Arguments
            -------------------------
            [`test_value`=None] {str}
                If provided, the file_path value must match this in order to return positively.

            [`default_val`=''] {any}
                The value to return of the file_path does not exist or does not match the test_value.


            Return {any}
            ----------------------
            If no test_value is provided the file_path value is returned.
            If a test_value is provided and the file_path value matches, the file_path is returned.

            If the file_path attribute does not exist or does not match the test_value,
            the default_val is returned.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-27-2022 11:55:25
            `memberOf`: drawing
            `version`: 1.0
            `method_name`: get_file_path
        '''

        if 'file_path' in self.data['file']:
            if test_value is not None:
                if self.data['file']['file_path'] == test_value:
                    return self.data['file']['file_path']
            else:
                return self.data['file']['file_path']
        return default_val


    @property
    def diagrams(self)->_Iterable[_Diagram]:
        '''
            Get this Drawing's diagrams


            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-04-2022 09:55:36
            `@memberOf`: Drawing
            `@property`: diagrams
        '''
        return _obj.get_arg(self.data,['diagrams'],[],(list))


def _get_diagrams(drawing:Drawing)->_Iterable[_diagram_type]:
    '''
        Parses the drawing to find all diagrams that it contains.
        This is used internally when reading a draw.io file.

        ----------

        Return {list}
        ----------------------
        A list of diagram instances, if no diagrams are found, the list is empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-27-2022 12:35:48
        `memberOf`: drawing
        `version`: 1.0
        `method_name`: get_diagrams
    '''

    result = []
    diagrams = drawing.tree.xpath("//diagram['@name']")
    if len(diagrams) > 0:
        d:_diagram_type
        for d in diagrams:
            result.append(_Diagram(drawing.tree,d))
    drawing.data['diagrams'] = result
    return result

