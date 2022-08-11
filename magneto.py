import inspect
import bdb


def hi(*args):
    print('hi') if args is None else print(*args)


class FrameAttributeMagnet(bdb.Bdb):
    """
        modified debugger to find specific
        attribute in a frame on a stack


        :param object_:
            object breakpoint insertion

        :param object_break_string_:
            string to find within object_

        :param break_offset_:
            number of lines after
            object_break_string_ object

        :param initiator_func_:
            function that is called
            to initiate the debugger

        :param initiator_func_args_:
            obvi

        :param magnetic_attribute_key_:
            key to retrieve corresponding
            value in specific attribute
            in frame local dict.


        example:
            *see display_magnet()
    """

    def __init__(
            self,
            object_,
            object_break_string_,
            break_offset_,
            initiator_func_,
            initiator_func_args_,
            magnetic_attribute_key_

    ):
        super().__init__()

        self.object_ = object_
        self.object_break_string_ = object_break_string_
        self.break_offset_ = break_offset_
        self.set_object_string_break()

        self.initiator_func_ = initiator_func_
        self.initiator_func_args_ = initiator_func_args_
        self.magnetic_attribute_key_ = magnetic_attribute_key_

        self.magnetic_frame_accumulator = []
        self.magnetic_member_accumulator = []
        self.magnetic_local_accumulator = []
        self.magnetic_attribute_accumulator = []
        self.find_frame()

    def user_line(self, frame):
        self.magnetic_frame_accumulator.append(frame)
        self.magnetic_member_accumulator.append(inspect.getmembers(frame))
        self.magnetic_local_accumulator.append(frame.f_locals)
        self.set_continue()

    def string_list_search(self, string_list_, search_term_):
        for elem_index_, elem_string_  in enumerate(string_list_):
            result_ = elem_string_.find(search_term_)
            if result_ > 0:
                return elem_index_

    def set_object_string_break(self):
        """
        find specific location within an *inspect* source lines object
        and insert a break point

        purpose is to mitigate the consequences of updated library files.
        for instance, if a function is developed to bypass standard library
        output or processes, a manual line number is can become invalidated
        fairly easily with the modification of a single line above a
        desired breakpoint. however, a breakpoint defined at a function
        variable assingment is more resilient because it would require the
        format of function to be changed at that specific line.
        """

        object_absfile_ = inspect.getabsfile(self.object_)
        object_sourcelines_info_ = inspect.getsourcelines(self.object_)

        object_sourcelines_ = object_sourcelines_info_[0]
        object_sourceline_num_ = object_sourcelines_info_[1]

        string_line_ = self.string_list_search(object_sourcelines_, self.object_break_string_)
        break_line_ = object_sourceline_num_ + string_line_ + self.break_offset_

        self.set_break(filename=object_absfile_, lineno=break_line_)

    def find_frame(self):
        self.runcall(self.initiator_func_, self.initiator_func_args_)
        # self.run(self.initiator_cmd_string_)
        # self.runeval(self.initiator_cmd_string_)

    def get_magnetic_attribute_accumulator(self):
        for local_dict in self.magnetic_local_accumulator:
            try:
                magnetic_attribute_temp = local_dict[self.magnetic_attribute_key_]

            except (KeyError, TypeError):
                magnetic_attribute_temp = "KeyError or TypeError"

            self.magnetic_attribute_accumulator.append(magnetic_attribute_temp)

        return self.magnetic_attribute_accumulator

    def get_magnetic_local_accumulator(self):
        return self.magnetic_local_accumulator

    def get_magnetic_member_accumulator(self):
        return self.magnetic_member_accumulator

    def get_magnetic_frame_accumulator(self):
        return self.magnetic_frame_accumulator


def display_magnet(display_object_, all_instances_=True, instance_position_=None):
    """
        IPython.display.display() does not return display data.
        display_magnet() retrieves display data.


        :param display_object_:
            IPython.display.display argument.
            ensure argument would otherwise display a figure.
            IPython can make multiple calls to display which
            produces multiple results.

        :param all_instances_:
            modifies return: list of all instances of display
            figure data.

        :param instance_position_:
            modifies return: one instance of list of all
            display figure data at position instance_position

        :return: magnetic_return_:
            element or whole list of mime data of display figure


        example:
            import numpy as np
            import matplotlib.pyplot as plt

            from magneto import FrameAttributeMagnet as fam


            plt.plot(np.random.normal(0, 1, (100, 100)))
            display_object_0 = plt.gcf()

            display_figure_data_0 = fam(display_object_0)
    """

    from ipykernel.jsonutil import encode_images
    from IPython.display import display

    object_ = encode_images
    object_break_string_ = 'return format_dict'
    break_offset_ = 0
    initiator_func_ = display
    initiator_func_args_ = display_object_
    magnetic_attribute_key_ = 'format_dict'

    frame_attribute_magnet = FrameAttributeMagnet(
        object_=object_,
        object_break_string_=object_break_string_,
        break_offset_=break_offset_,
        initiator_func_=initiator_func_,
        initiator_func_args_=initiator_func_args_,
        magnetic_attribute_key_=magnetic_attribute_key_
    )

    magnetic_attributes_ = frame_attribute_magnet.get_magnetic_attribute_accumulator()
    # magnetic_locals_ = frame_attribute_magnet.get_magnetic_local_accumulator()
    # magnetic_members_ = frame_attribute_magnet.get_magnetic_member_accumulator()
    # magnetic_frames_ = frame_attribute_magnet.get_magnetic_frame_accumulator()

    if all_instances_ and instance_position_ is None:
        magnetic_return_ = magnetic_attributes_
    else:
        magnetic_return_ = magnetic_attributes_

    return magnetic_return_
