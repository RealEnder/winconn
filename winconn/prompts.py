### BEGIN LICENSE
# Copyright (C) 2012 Alex Stanev <alex@stanev.org>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

#import Gtk
#import gobject
#import GLib
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib

import os
import locale
from locale import gettext as _
locale.textdomain('quickly-widgets')

#TODO: stop using **kwargs and go back to named arguments so you can pass them from the function to the class

class Prompt(Gtk.Dialog):
    """A base class for some quickly.prompts - creates Ok and Cancel buttons,
    displays a title and a label.

    qiuckly.prompts.Prompt is intended for receiving information back
    from users. If you only want to display a message, use a
    quickly.prompts.Alert.

    Useful subclasses and helper functions are provided:
    quickly.prompts.string() uses quickly.prompts.StringPrompt
    quickly.prompts.date() uses quickly.prompts.DatePrompt
    quickly.prompts.integer() uses quickly.prompts.IntegerPrompt
    quickly.prompts.decimal() uses quickly.prompts.DecimalPrompt
    quickly.prompts.price() uses quickly.prompts.PricePrompt

    Using
    A quickly.prompts.prompt object is not intended to be used without
    configuring or extending it. Otherwise, it will only display a 
    blank dialog with OK and Cancel buttons and a label.

    Configuring
    #add some widgets to the prompt using the
    #the prompt's content_box member (which is a Gtk.VBox)
    #These widgets will appear below the label
    #StringPrompt works similar to this:
    p = quickly.prompts.Prompt(title,text)
    entry = Gtk.Entry()
    entry.set_text(default_value)
    entry.set_activates_default(True)
    entry.show()
    p.content_box.pack_end(entry, True, True, 5)
    response = p.run()
    if response = Gtk.ResponseType.OK:
        my_string = entry.get_text()

    #A Prompt is a Gtk.Dialog, so you can use Gtk.DialogMembers
    action_area = p.get_action_area()

    Extending 
    #Typically you will add widgets to a prompt and override the
    #get_value function to return the appropriate value entered by the user.
    #String prompt is implemented as follows:
    class StringPrompt(Prompt):
        def __init__(self, title = "Input String",
                     text = "Input a String:", default_value = ""):
            Prompt.__init__(self, title, text)
            self._entry = Gtk.Entry()
            self._entry.set_text(default_value)
            self._entry.set_activates_default(True)
            self._entry.show()
            self.content_box.pack_end(self._entry, True, True, 5)
    
        def get_value(self):
                return self._entry.get_text()

    """

    def __init__(self, title, text):
        """Creates a Prompt
        arguments:
        title - The title for the dialog window
        text -  The string to display in the Prompts label

        """

        Gtk.Dialog.__init__(self, title, None, Gtk.DialogFlags.MODAL,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        #self.set_has_separator(False)
        content_area = self.get_content_area()
        content_area.set_border_width(5)
        self.set_default_response(Gtk.ResponseType.OK)

        self.content_box = Gtk.VBox(False, 10)
        label = Gtk.Label(text)
        label.set_line_wrap(True)
        self.content_box.pack_start(label,False, False, 5)
        content_area.pack_start(self.content_box,False, False, 5)
        self.content_box.show()
        label.show()

def string(title = _("Input String"), text = _("Input a String:"), default_value = ""):
    """string - prompts to enter a string via a dialog box.

    aguments:
    title - a string to be the title of the dialog
    text - a string to provide a prompt for the user within dialog
    default_value - a string to see the entry in the dialog box

    returns a tuple of (Gtk.DialogResponse, string value)
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)

    """

    sp = StringPrompt(title, text, default_value)
    response = sp.run()
    val = sp.get_value()
    sp.destroy()
    return (response, val)

class StringPrompt(Prompt):
    """A class for receiving a string from a user

    Using
    #Collect a string from the user by using the
    #quickly.prompts.string() helper function
    reponse, val = string("String select test","String select test")
    if response == Gtk.ResponseType.OK:
        my_string = val

    Configuring
    #Add widgets to the conent_box member
    sp = StringPrompt(title, text, default_string)
    sp.content_box.pack_end(my_additional_widget, False, False, 5)

    #Modify the _entry member
    sp._entry.set_max_length(144)

    Extending
    A StringPrompt is a Prompt which is Gtk.Dialog

    """

    def __init__(self, title = _("Input String"), text = _("Input a String:"), default_value = ""):
        """Create a StringPrompt
        arguments:
        title - a string to be the title of the dialog
        text - a string to provide a prompt for the user within dialog
        default_value - a string to see the entry in the dialog box

        """

        Prompt.__init__(self, title, text)
        self._entry = Gtk.Entry()
        self._entry.set_text(default_value)
        self._entry.set_activates_default(True)
        self._entry.show()
        self.content_box.pack_end(self._entry, True, True, 5)

    def get_value(self):
        """get_value - returns the value the user has entered into the Gtk.Entry

        """

        return self._entry.get_text()

def date(title = _("Choose Date"), text = _("Choose a Date:"), default_value = None):
    """date - prompts to enter a date using a calendar via a dialog box.

    aguments:
    title - a string to be the title of the dialog
    text - a string to provide a prompt for the user within dialog
    default_value - a tuple in the form of integers for (year,month,day)
    where month is zero indexed (Jaunary is 0, December is 11)

    returns a tuple of (Gtk.DialogResponse, tuple)
    The returnd tuple is in the form of integers for (year,month,day)
    where month is zero indexed (Jaunary is 0, December is 11)

    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)

    """
    dp = DatePrompt(title, text, default_value)

    response = dp.run()
    val = dp.get_value()
    dp.destroy()
    return (response, val)

class DatePrompt(Prompt):
    """A class for receiving a date from a user

    Using
    #Collect a date from the user by using the
    #quickly.prompts.date() helper function
    reponse, val = date("Date prompt title","Date prompt message")
    if response == Gtk.ResponseType.OK:
        my_date = val

    Configuring
    #Add widgets to the content_box member
    dp = DatePrompt(title, text, default_integer)
    dp.content_box.pack_end(my_additional_widget)

    #Modify the _calendar member
    dp._calendar.set_display_options(Gtk.CALENDAR_SHOW_DAY_NAMES)

    Extending
    A DatePrompt is a Prompt which is a Gtk.Dialog.

    """

    def __init__(self, title = _("Choose Date"), text = _("Choose a Date:"), default_value = None):
        """Creates a DatePrompt
        title - a string to be the title of the dialog
        text - a string to provide a prompt for the user within dialog
        default_value - a tuple in the form of integers for (year,month,day)
        where month is zero indexed (Jaunary is 0, December is 11)

        """
        Prompt.__init__(self, title, text)          
        self._calendar = Gtk.Calendar()
        self._calendar.show()
        self.content_box.pack_end(self._calendar, True, True, 5)

        if default_value is not None and len(default_value) is 3:
            year, month, day = default_value
            self._calendar.select_month(month, year)
            self._calendar.select_day(day)

    def get_value(self):
        """get_value - return the date currently set in the _calendar member
        A tuple is in the form of integers for (year,month,day)
        where month is zero indexed (Jaunary is 0, December is 11)

        """

        return self._calendar.get_date()

def integer(title = _("Enter Number"), text = _("Enter an Integer Value:"), 
            default_value=0, min_value = -1000000000, max_value=1000000000,
            step = 1):
    """integer - prompts to enter an integer using a spinner via a dialog box.

    arguments:
    title - a string to be the title of the dialog
    text - a string to provide a prompt for the user within dialog
    default_value - an integer to display by default, should be greater than

    keyword arguments:
    the min_value and less then the max_value
    min_value - the lowest number accepted by the spinner, 
    defaults to -1000000000
    step - set the incriments for each click of the spinner buttons,
    defaults to 1
    max_value, the highest number accepted by the spinner,
    defaults to 1000000000

    returns a tuple of (Gtk.DialogResponse, integer)

    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)

    """

    ip = IntegerPrompt(title,text,default_value, min_value, max_value, step)
    response = ip.run()
    val = ip.get_value()
    ip.destroy()
    return (response, val)


class IntegerPrompt(Prompt):
    """A Prompt for collecting an integer number value from user. Uses
        a Gtk.Spinner for data entry.


    Using
    #Collect an integer value from the user by using the
    #quickly.prompts.integer() helper function
    reponse, val = integer("Integer prompt title","Integer prompt message")
    if response == Gtk.ResponseType.OK:
        my_date = val

    Configuring
    #Add widgets to the content_box member
    dp = IntegerPrompt(title, text, default_date)
    dp.content_box.pack_end(my_additional_widget)

    #Modify the _spinner member
    dp._spinner.set_value(20)

    Extending
    An IntegerPrompt is a Prompt which is a Gtk.Dialog

    """

    def __init__(self, title=_("Enter Number"), text=_("Enter an Integer Value:"),
            default_value=0, min_value = -1000000000, max_value=1000000000,
            step = 1):
        """Creates an Integer Prompt

        """

        Prompt.__init__(self, title, text)
        adj = Gtk.Adjustment(default_value,min_value,max_value,step)
        self._spinner = Gtk.SpinButton()
        self._spinner.set_adjustment(adj)
        self._spinner.set_activates_default(True)
        self._spinner.show()
        self._spinner.set_numeric(True)
        self.content_box.pack_end(self._spinner, True, True, 5)

    def get_value(self):
            return self._spinner.get_value_as_int()

def decimal(title=_("Enter Price"), text=_("Choose a Price:"), 
          default_value=0, min_value=-1000000000, max_value=1000000000,
          step=1,digits=20):
    """decimal - prompts to enter a number that inlcudes
    decimal places using a spinner via a dialog box.

    aguments:
    title - a string to be the title of the dialog
    text - a string to provide a prompt for the user within dialog

    keyword arguments:
    default_value - an integer to display by default, should be greater than
    the min_value and less then the max_value
    min_value - the lowest number accepted by the spinner, 
    defaults to -1000000000
    step - set the incriments for each click of the spinner buttons,
    defaults to 1
    max_value, the highest number accepted by the spinner,
    defaults to 1000000000
    digits - the number of decimal places to include, defaults to 20
    supports a maximum of 20 decimal places. Values great than 20 will
    be converted to 20, and values less than 0 will be converted to 0

    returns a tuple of (Gtk.DialogResponse, number)

    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)

    """

    dp = DecimalPrompt(title, text, default_value, min_value, max_value,
                       step, digits)
    response = dp.run()
    val = dp.get_value()
    dp.destroy()
    return (response, val)

class DecimalPrompt(Prompt):
    """A Prompt for collecting a decimal number value from user. Uses
        a Gtk.Spinner for data entry.

    Using
    #Collect a number from the user by using the
    #quickly.prompts.decimal() helper function
    reponse, val = decimal("Decimal prompt title","Decimal prompt message")
    if response == Gtk.ResponseType.OK:
        my_decimal = val

    Configuring
    #Add widgets to the content_box member
    dp = DecimalPrompt(title, text, default_number)
    dp.content_box.pack_end(my_additional_widget)

    #Modify the _spinner member
    dp._spinner.set_value(20.0)

    Extending
    An DecimalPrompt is a Prompt which is a Gtk.Dialog


    """

    def __init__(self, title=_("Enter Number"), text=_("Enter an Integer Value:"),
                    default_value=0, min_value=-1000000000, max_value=1000000000,
                    step=1, digits=20):
        """Creates a DecimalPrompt
        arguments:
        title - a string to be the title of the dialog
        text - a string to provide a prompt for the user within dialog
        default_value - an integer to display by default, should be greater than

        keyword arguments:
        default_value - an integer to display by default, should be greater than
        the min_value and less then the max_value
        min_value - the lowest number accepted by the spinner, 
        defaults to -1000000000
        step - set the incriments for each click of the spinner buttons,
        defaults to 1
        max_value, the highest number accepted by the spinner,
        defaults to 1000000000
        digits - the number of decimal places to include, defaults to 20
        supports a maximum of 20 decimal places. Values great than 20 will
        be converted to 20, and values less than 0 will be converted to 0

        returns a tuple of (Gtk.DialogResponse, number)
    
        Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
        the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
        (Gtk.ResponseType.DELETE_EVENT)

        """

        Prompt.__init__(self, title, text)

        self._adjustment = Gtk.Adjustment(default_value,min_value,max_value,step)
        if digits > 20:
            digits = 20
        if digits < 0:
            digits = 0
        self._spinner = Gtk.SpinButton()
        self._spinner.set_adjustment(self._adjustment)
        self._spinner.set_digits(digits)
        self._spinner.set_activates_default(True)
        self._spinner.show()
        self._spinner.set_numeric(True)
        self.content_box.pack_end(self._spinner, True, True, 5)

    def get_value(self):
            return self._spinner.get_value()

def price(title=_("Enter Price"), text=_("Choose a Price:"), 
          default_value=0, min_value=-1000000000, max_value=1000000000,
          step=1):
    """price - prompts to enter a number up to the 
    hundreths place using a spinner via a dialog box.

    aguments:
    title - a string to be the title of the dialog
    text - a string to provide a prompt for the user within dialog
    default_value - an integer to display by default, should be greater than

    keyword arguments:
    the min_value and less then the max_value
    min_value - the lowest number accepted by the spinner, 
    defaults to -1000000000
    max_value, the highest number accepted by the spinner,
    defaults to 1000000000
    step - set the incriments for each click of the spinner buttons,
    defaults to 1

    returns a tuple of (Gtk.DialogResponse, number)

    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)

    """

    pp = PricePrompt(title, text, default_value, min_value, max_value,
                       step)
    response = pp.run()
    val = pp.get_value()
    pp.destroy()
    return (response, val)

class PricePrompt(DecimalPrompt):
    """A Prompt for collecting a decimal number value from the user,
        formatted with two decimal places appropriate for entering
        a currence ammount. Uses a Gtk.Spinner for data entry.

    Using
    #Collect a number from the user by using the
    #quickly.prompts.price() helper function
    reponse, val = price("Price prompt title","Price prompt message")
    if response == Gtk.ResponseType.OK:
        my_date = val

    Configuring
    #Add widgets to the content_box member
    pp = PricePrompt(title, text, default_number)
    pp.content_box.pack_end(my_additional_widget)

    #Modify the _spinner member
    pp._spinner.set_value(20.00)

    Extending
    An PricePrompt is Decimal Prompt which is a Prompt which is a Gtk.Dialog


    """

    def __init__(self, title=_("Enter Price"), text=_("Choose a Price:"), 
          default_value=0, min_value=-1000000000, max_value=1000000000,
          step=1):
        """Creates a DecimalPrompt
        arguments:
        title - a string to be the title of the dialog
        text - a string to provide a prompt for the user within dialog
        default_value - an integer to display by default, should be greater than

        keywrod arguments:
        keyword arguments:
        the min_value and less then the max_value
        min_value - the lowest number accepted by the spinner, 
        defaults to -1000000000
        max_value, the highest number accepted by the spinner,
        defaults to 1000000000
        step - set the incriments for each click of the spinner buttons,
        defaults to 1

        returns a tuple of (Gtk.DialogResponse, number)

        Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
        the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
        (Gtk.ResponseType.DELETE_EVENT)

        """

        DecimalPrompt.__init__(self,title,text,default_value,min_value,
                              max_value, step)
        self._spinner.set_digits(2)

def yes_no(title = _("Choose Yes or No"), text = "", yes="", no=""):
    """yes_no - prompts the user to choose between two options,
        one "yes" and one "no", though typically the button labels
        should be set as verbs.

    aguments:
    title - a string to be the title of the dialog
    text - a string, typically a question, prompting the
    user to choose Yes or No
    yes - a string that is a verb representing the Yes action
    no - a string that is a verb representing the No action

    returns a Gtk.DialogResponse
    Gtk.ResponseType.YES means the user clicked the "YES" button, otherwise
    Gtk.ResponseType.NO means the user clicked the "NO" button, otherwise
    the user dismissed the dialogv(Gtk.ResponseType.DELETE_EVENT)

    """
    yn = YesNoPrompt(title,text,yes,no)
    response = yn.run()
    yn.destroy()
    return response

class YesNoPrompt(Gtk.Dialog):
    """A prompt to collect a user choice between two options,
        one "yes" and one "no", though typically the button labels
        should be set as verbs.

    Using
    #Collect a response from the user using the
    #quickly.prompts.yes_no() helper function
    reponse = decimal(title,message,"Do it", "Don't do it")
    if response == Gtk.ResponseType.YES:
        yes = True
    else:
        yes = False

    Configuring
    #Add widgets to the content_box member
    dp = DecimalPrompt(title, text, default_number)
    dp.content_box.pack_end(my_additional_widget)

    #add a widget to the response by creating it and
    #passing it in with a Gtk.ResponseType.ID
    dp.add_action_widget(new_widget, response_id)

    Extending
    An YesNoPrompt is a Gtk.Dialog

    """

    def __init__(self, title=_("Choose an option"),text="",yes="",no=""):
        """creaets a YesNoPrompt.
        
        aguments:
        title - a string to be the title of the dialog
        text - a string, typically a question, prompting the
        user to choose Yes or No
        yes - a string that is a verb representing the Yes action
        no - a string that is a verb representing the No action

        """

        Gtk.Dialog.__init__(self, title, None, Gtk.DialogFlags.MODAL)

        if no == "":
            no_button = Gtk.Button(stock=Gtk.STOCK_NO)
        else:
            no_button = Gtk.Button(label=no, use_underline=True)
        self.add_action_widget(no_button,Gtk.ResponseType.NO)
        no_button.show()

        if yes == "":
            yes_button = Gtk.Button(stock=Gtk.STOCK_YES)
        else:
            yes_button = Gtk.Button(label=yes, use_underline=True)
        self.add_action_widget(yes_button,Gtk.ResponseType.YES)
        yes_button.show()
        yes_button.set_can_default(True)


        #self.set_has_separator(False)
        content_area = self.get_content_area()
        content_area.set_border_width(5)
        self.set_default_response(Gtk.ResponseType.YES)

        self.content_box = Gtk.HBox(False, 10)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_DIALOG_QUESTION,Gtk.IconSize.DIALOG)
        self.content_box.pack_start(img, False, False, 5)
        label = Gtk.Label(text)
        label.set_line_wrap(True)
        self.content_box.pack_start(label,False, False, 5)
        content_area.pack_start(self.content_box, False, False, 5)
        self.content_box.show()
        label.show()
        img.show()

def warning(title = _("Warning"), text = ""):
    """warning - displays a warning to the user, includes an appropriate icon
    and an OK button

    aguments:
    title - a string to be the title of the dialog
    text - a string describing the warning

    returns a Gtk.DialogResponse
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user dismissed the dialogv(Gtk.ResponseType.DELETE_EVENT)

    """

    w = Alert(title,text,Gtk.STOCK_DIALOG_WARNING)
    response = w.run()
    w.destroy()
    return response

def error(title = _("Error"), text = ""):
    """error - displays an error to the user, includes an appropriate icon
    and an OK button

    aguments:
    title - a string to be the title of the dialog
    text - a string describing the error

    returns a Gtk.DialogResponse
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user dismissed the dialogv(Gtk.ResponseType.DELETE_EVENT)

    """

    e = Alert(title,text,Gtk.STOCK_DIALOG_ERROR)
    response = e.run()
    e.destroy()
    return response


def info(title = _("Information"), text = ""):
    """info - displays information to the user, includes an appropriate
    icon and an OK button

    aguments:
    title - a string to be the title of the dialog
    text - a string providing the information

    returns a Gtk.DialogResponse
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user dismissed the dialogv(Gtk.ResponseType.DELETE_EVENT)

    """

    i = Alert(title,text,Gtk.STOCK_DIALOG_INFO)
    response = i.run()
    i.destroy()
    return response

class Alert(Gtk.Dialog):
    """Displays an icon, a message, and an OK button to users.
    Used by quickly.prompts.info(), quickly.prompts.warning(),
    and quickly.prompts.error(). 

    Using
    #Display a message to the user using one of the helper functions
    quickly.prompts.info(title,useful_message)

    Configuring
    #Add widgets to the content_box member
    alert = Alert(title, text, image)
    alert.content_box.pack_end(my_additional_widget, False, False, 5)

    #change the image by passing in a stock Gtk image
    alert.set_image(stock_image)

    Extending
    An Alert is a Gtk.Dialog.

    """

    def __init__(self,title="",text="",image=None):
        Gtk.Dialog.__init__(self, title,None,Gtk.DialogFlags.MODAL,(Gtk.STOCK_OK, Gtk.ResponseType.OK))
        #self.set_has_separator(False)
        content_area = self.get_content_area()
        content_area.set_border_width(5)
        self.set_default_response(Gtk.ResponseType.OK)

        self.content_box = Gtk.HBox(False, 10)
        label = Gtk.Label(text)
        label.set_line_wrap(True)
        self._image = Gtk.Image()
        self._image.set_from_stock(image,Gtk.IconSize.DIALOG)
        self.content_box.pack_start(self._image, False, False, 5)
        self.content_box.pack_end(label,False, False, 5)
        content_area.pack_start(self.content_box, False, False, 5)
        self.content_box.show()
        label.show()
        self._image.show()

    def set_image(self, image):
        self._image.set_from_stock(image,Gtk.IconSize.DIALOG)        
    

def save_image_file(title=_("Choose an Image"),path=None):
    """save_image_file - prompts the user to choose an image file

    aguments:
    title - a string to be the title of the dialog
    path - a string providing a path to a directory where the
    dialog should start. Defaults to Pictures directory.

    returns a Gtk.DialogResponse
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user clicked "Cancel" or the userdismissed the 
    dialogv(Gtk.ResponseType.DELETE_EVENT)

    """

    sid = SaveImageDialog(title,path)
    response = sid.run()
    value = sid.get_filename()
    sid.destroy()
    return (response, value)


class ImageDialog(Gtk.FileChooserDialog):
    """A base class for OpenImageDialog and SaveImageDialog

    Sets up typical mime types and file name patterns suitable
    for saving images.

    This class is not typically used configured or extended directly,
    but rather through OpenImageDialog and SaveImageDialog.

    """


    def __init__(self, action, button, title="", path=None):
        """Create an ImageDialog.

        arguments:
        action - a file chooser action, either Gtk.FILE_CHOOSER_ACTION_SAVE
        or Gtk.FILE_CHOOSER_ACTION_OPEN
        button - a Gtk stock button for the intended action, either
        Gtk.STOCK_SAVE or Gtk.STOCK_OPEN

        keyword arguments:
        title - a title for the dialog, defaults to an empty string
        path - a directory path to initially open to, defaults to 
        ~/Pictures

        """

        Gtk.FileChooserDialog.__init__(self,title,
                                            None,
                                            action,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            button, Gtk.ResponseType.OK))

        self.set_default_response(Gtk.ResponseType.OK)

        if path == None:
            path = GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES)        
        self.set_current_folder(path)

        self._filter = Gtk.FileFilter()
        self._filter.set_name("All files")
        self._filter.add_pattern("*")
        self.add_filter(self._filter)

        self._filter = Gtk.FileFilter()
        self._filter.set_name("Images")
        self._filter.add_mime_type("image/png")
        self._filter.add_mime_type("image/jpeg")
        self._filter.add_mime_type("image/gif")
        self._filter.add_pattern("*.png")
        self._filter.add_pattern("*.jpg")
        self._filter.add_pattern("*.gif")
        self._filter.add_pattern("*.tif")
        self._filter.add_pattern("*.xpm")
        self.add_filter(self._filter)
        self.set_do_overwrite_confirmation(True)          

class SaveImageDialog(ImageDialog):
    """
    A dialog to prompt the user for a place to save an image file.

    Using
    #Collect a location using the quickly.prompts.save_image_file()
    #helper function
    response, path = save_image_file(title)
    if response == Gtk.ResponseType.OK:
        save_to_path = path

    Configuring
    #Modify the _filter member
    sid._filter.add_mime_type("image/svg")
    sid._filter.add_pattern("*.svg")

    Extending
    A SaveImageDialog is an ImageDialog which is a Gtk.FileChooserDialog

    """

    def __init__(self, title="Choose File Location", path=None):
        """Create a SaveImageDialog.

        keyword arguments:
        title - a title for the dialog, defaults to an empty string
        path - a directory path to initially open to, defaults to 
        ~/Pictures

        """

        ImageDialog.__init__(self,Gtk.FileChooserAction.SAVE, Gtk.STOCK_SAVE, title,path)

class OpenImageDialog(ImageDialog):
    """
    A dialog to prompt the user for an image to open

    Using
    #Collect a location using the quickly.prompts.open_image_file()
    #helper function
    response, path = open_image_file(title)
    if response == Gtk.ResponseType.OK:
        path_to_image = path

    Configuring
    #Modify the _filter member
    sid._filter.add_mime_type("image/svg")
    sid._filter.add_pattern("*.svg")

    Extending
    A SaveImageDialog is an ImageDialog which is a Gtk.FileChooserDialog

    """

    def __init__(self, title="Choose File Location", path=None):
        """Create an OpenImageDialog.

        keyword arguments:
        title - a title for the dialog, defaults to an empty string
        path - a directory path to initially open to, defaults to 
        ~/Pictures

        """
        ImageDialog.__init__(self,Gtk.FileChooserAction.OPEN, Gtk.STOCK_OPEN, title,path)

def open_image_file(title=_("Choose an Image"),path=None):
    """open_image_file - prompts the user to choose an image file

    aguments:
    title - a string to be the title of the dialog
    path - a string providing a path to a directory where the
    dialog should start. Defaults to Pictures directory.

     returns a tuple of (Gtk.DialogResponse, str)
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)
    The str is the path to the image chosen by the user, if any.


    """

    oid = OpenImageDialog(title,path)
    response = oid.run()
    value = oid.get_filename()
    oid.destroy()
    return (response, value)

def choose_directory(title=_("Choose a Directory"),path=None):
    """choose_directory - prompts the user to choose an directory

    aguments:
    title - a string to be the title of the dialog
    path - a string providing a path to a directory where the
    dialog should start.


    returns a tuple of (Gtk.DialogResponse, str)
    Gtk.ResponseType.OK means the user clicked the "OK" button, otherwise
    the user cancelled (Gtk.ResponseType.CANCEL) or dismissed the dialog
    (Gtk.ResponseType.DELETE_EVENT)
    The str is the path to the directory chosen by the user, if any.

    """

    dcd = DirectoryChooserDialog(title, path)
    response = dcd.run()
    value = dcd.get_filename()
    dcd.destroy()
    return (response, value)

class DirectoryChooserDialog(Gtk.FileChooserDialog):
    """A Dialog to prompt the user to choose a directory path.

    Using
    #prompt the user to provide a directory path using 
    quickly.prompts.choose_directory(title)

    Configuring
    #A DirectoryChooseDialog is a Gtk.FileChooserDialog, so you can
    #use Gtk.FileChooseDialog members
    dcd = DirectoryChooserDialog(title)
    dcd.set_local_only(False)

    Extending
    #A DirectoryChooseDialog is a Gtk.FileChooserDialog

    """

    def __init__(self, title, path=None):
        """Creates a DirectoryChooseDialog

        arguments:
        title - A title for the dialog

        keyword arguments:
        path - a default location for opening the dialogs

        """

        Gtk.FileChooserDialog.__init__(self, title,
                                    None,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.set_default_response(Gtk.ResponseType.OK)
        if path is not None:
            self.set_current_folder(path)


if __name__ == "__main__":
    """test code to try out the dialogs"""
    #these don't have return values to test for
    warning("Warning Prompt","Warning Prompt")
    info("Information Prompt","Information Prompt")
    error("Error Prompt","Error Prompt")

    #the rest of values to test for
    response, val = choose_directory("directory choose test")
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "selected directory was " + str(val)

    response, val = open_image_file("image open test")
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "selected locations was " + str(val)

    response, val = save_image_file("image save test")
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "selected locations was " + str(val)

    reponse, val = string("String select test","String select test")
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "string was " + str(val)

    reponse, val = date("Date select test","Date select test")
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "date was " + str(val)

    reponse, val = integer("Integer select test","Integer select test",default_value=20)
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "integer was " + str(val)

    reponse, val = decimal("Decimal select test","Decimal select test",default_value=20,digits=5)
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "decimal was " + str(val)

    reponse, val = price("Price select test","Price select test",default_value=20)
    if response == Gtk.ResponseType.OK:
        print "response was OK"
    else:
        print "response was not OK"
    print "price was " + str(val)

    response = yes_no("Yes/No Test","Yes/No Test", "_Yes Verb","_No Verb")
    if response == Gtk.ResponseType.YES:
        print "response was yes"


