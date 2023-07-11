import yaml


class Texts:
    def __init__(self) -> None:
        self.yaml_path = "texts.yml"
        self.wellcome_wa_text = 'Здравствуйте, {0}! \
Меня зовут Домиант, я Ваш бот-помощник, работаю консъержем в доме {1}. \
Я могу передать информацию управляющему, председателю или секретарю собраний.'

        self.wa_notification = """На указанную вами почту {0} отправлено письмо с заполненным бюллетенем для голосования. 
Прошу без задержки направить его ответным письмом (нажать кнопку ответить затем нажать отправить).

Спасибо за участие в делах дома!
С уважением, секретарь собрания."""

    def wa_posts(self):
        with open(self.yaml_path, "r") as stream:
            try:
                texts = yaml.safe_load(stream)
                return texts['texts']['whatsapp']
            except yaml.YAMLError as exc:
                print(exc)

    def update_wa_texts(self, message=None, value=None):
        with open(self.yaml_path, "r") as stream:
            try:
                texts = yaml.safe_load(stream)
                texts['texts']['whatsapp'][message] = value
            except yaml.YAMLError as exc:
                print(exc)
        with open(self.yaml_path, "w") as stream:
            try:
                yaml.safe_dump(texts, stream, allow_unicode=True)
            except yaml.YAMLError as exc:
                print(exc)

    def append_wa_text(self, message=None, value=None):
        with open(self.yaml_path, "r") as stream:
            try:
                texts = yaml.safe_load(stream)
                texts['texts']['whatsapp'][message] = value
            except yaml.YAMLError as exc:
                print(exc)
        with open(self.yaml_path, "w") as stream:
            try:
                yaml.safe_dump(texts, stream, allow_unicode=True)
            except yaml.YAMLError as exc:
                print(exc)


if __name__ == "__main__":
    texts = Texts()
    print(texts.wa_posts()["wellcome_message"].format(
        "cur_name", "cur_address"))
