def centralize_text(some_text: str) -> str:
    return "<center>" + some_text + "</center>"


def copy_xl_template(prefix: str = 'empty', new_name: str = 'Документы\\newfile.xlsx'):
    try:
        with open("static\\" + prefix + "template.xlsx", 'rb') as first:
            with open(new_name, 'wb') as result:
                result.write(first.read())
        return True
    except:
        return False
