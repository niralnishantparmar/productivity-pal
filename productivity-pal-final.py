#Imports
import flet as ft
from flet import Checkbox, FloatingActionButton, Page, TextField, icons
import math

#----------------------------------------------------CHAT APP----------------------------------------------------
class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type
        alignment=ft.alignment.center


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        # self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(message.user_name[:1].capitalize()),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Productivity Pal"
    '''
    page.fonts = {
        "Montserrat" : "https://raw.github.com/JulietaUla/Montserrat/fonts/otf/Montserrat-Regular.otf",
        "Montserrat-Black": "\fonts\Montserrat-Black.ttf",
    }
    #page.theme = Theme(font_family="Montserrat")
    '''
    #when the user joins the chat room----------------------------------------------
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank! Sorry."
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.",
                        message_type="login_message"))
            page.update()

    #when the user sends a message----------------------------------------------------
    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    #The "what is your name" part (when you initially open the service) ----------------------------------------------------
    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    # chat view ----------------------------------------------------
    chat = ft.ListView(
        expand=True,
        spacing=10,
        #alignment=ft.alignment.center,
        auto_scroll=True,
    )

    #User input for messages ----------------------------------------------------
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,   
        bgcolor=(ft.colors.LIGHT_GREEN_100),#'#c4e3c7',     
        on_submit=send_message_click,
    )

#----------------------------------------------------HEADER----------------------------------------------------

    #page.add(ft.Icon(name="ACCESS_TIME_FILLED_OUTLINED"))
    #label = ft.Text(text_align='center', value='This is Header', size='32', style='bold', color='blue')
    page.add(
        ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "ProductivityPal - your go-to collaborative to-do app",
                            ft.TextStyle(
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                #alignment=ft.alignment.center,
                                 #= 'center',
                                foreground=ft.Paint(  
                                    #color=ft.colors.BLUE_700,
                                    gradient=ft.PaintLinearGradient(
                                    (0, 20), (215, 20), [ft.colors.LIGHT_GREEN_400, ft.colors.GREEN, ft.colors.LIGHT_GREEN_100]
                                    ),
                                    stroke_width=6,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "ProductivityPal - your go-to collaborative to-do app",
                            ft.TextStyle(
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                            ),
                        ),
                    ],
                ),
            ]
        )
    )
    #Chat Widget ------------
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )
    #----------------------------------------------------TO-DO APP----------------------------------------------------
    def add_clicked(e):
        page.add(Checkbox(label=new_task.value))
        new_task.value = "" 
        page.update()

    new_task = TextField(hint_text="Write your task here, and select the plus icon to confirm it.", bgcolor=(ft.colors.LIGHT_GREEN_100))
    page.add(new_task, FloatingActionButton(icon=icons.ADD, on_click=add_clicked, bgcolor=(ft.colors.GREEN)))
'''
    def __init__(self, task_name):
        self.task_name = task_name

    def build(self):
        self.display_task = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(expand=1)
       

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
    
    
    '''





#Run app
ft.app(port=8500, target=main, assets_dir="assets", view=ft.WEB_BROWSER)
