#**************************************************************************
# 
# This material was prepared by the Los Alamos National Security, LLC 
# (LANS), under Contract DE-AC52-06NA25396 with the U.S. Department of 
# Energy (DOE). All rights in the material are reserved by DOE on behalf 
# of the Government and LANS pursuant to the contract. You are authorized 
# to use the material for Government purposes but it is not to be released 
# or distributed to the public. NEITHER THE UNITED STATES NOR THE UNITED 
# STATES DEPARTMENT OF ENERGY, NOR LOS ALAMOS NATIONAL SECURITY, LLC, NOR 
# ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR 
# ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, 
# COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR 
# PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE 
# PRIVATELY OWNED RIGHTS.
# 
#**************************************************************************

class __OneTimeCustomException(Exception):
    pass


try:
    try:
        import pyjd
        if not pyjd.is_desktop:
            raise __OneTimeCustomException('Compiling with pyjs.')
    except ImportError:
        pass

    ## WxPython


    from datetime.datetime import strptime
    from flex_ui import FlexUI, multiline_text
    UserInterface = FlexUI

except __OneTimeCustomException:
    ## Pyjamas
    from pyjamas import Window
    from pyjamas.ui.RootPanel import RootPanel
    from pyjamas.ui.SimplePanel import SimplePanel
    from pyjamas.ui.DecoratorPanel import DecoratedTabPanel
    from pyjamas.ui.DecoratorPanel import DecoratorPanel
    from pyjamas.ui.DecoratorPanel import DecoratorTitledPanel
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.Image import Image
    from pyjamas.ui.HTML import HTML
    from pyjamas.ui.Button import Button
    from pyjamas.ui.RadioButton import RadioButton
    from pyjamas.ui.FlexTable import FlexTable
    from pyjamas.ui.Label import Label
    from pyjamas.ui.CheckBox import CheckBox
    from pyjamas.ui.TextArea import TextArea
    from pyjamas.ui.TextBox import TextBox
    from pyjamas.ui.Calendar import DateField
    from pyjamas.ui.Calendar import Calendar
    from pyjamas.ui import HasAlignment

    try:
        import gchartplot as plotter
    except:
        try:
            import raphaelplot as plotter
        except:
            raise ImportError('No plotting modules available')

    from web_ui import WebUI, strptime, multiline_text
    UserInterface = WebUI