import configparser


def parseConfig(file, section):
    conf = configparser.ConfigParser()
    conf.read(file, encoding='utf-8')
    items = conf.items(section)
    return dict(items)
