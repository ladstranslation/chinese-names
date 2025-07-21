from flask import Flask, render_template, request, jsonify
import json
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)

# Load the names database from JSON
NAMES_DATA = {
  "Abagail": {
    "chinese": "阿芭给尔",
    "pinyin": "ā bā gěi ěr",
    "meaning": "a, fragrant plant, give, you (classical)"
  },
  "Abby": {
    "chinese": "阿碧",
    "pinyin": "ā bì",
    "meaning": "a + jade"
  },
  "Abigail": {
    "chinese": "阿碧给尔",
    "pinyin": "ā bì gěi ěr",
    "meaning": "a + jade + give + you (classical)"
  },
  "Acacia": {
    "chinese": "阿卡霞",
    "pinyin": "ā kǎ xiá",
    "meaning": "a + ka, sunset/rosy sky"
  },
  "Acella": {
    "chinese": "阿璱拉",
    "pinyin": "ā sè lā",
    "meaning": "bright jade pulls"
  },
  "Adliya": {
    "chinese": "阿蒂拉",
    "pinyin": "ā dì lā",
    "meaning": "a + flower stem, pull"
  },
  "Adrianna": {
    "chinese": "阿达丽安娜",
    "pinyin": "ā dá lì ān nà",
    "meaning": "a + reach + beautiful + peace + graceful"
  },
  "Adrienne": {
    "chinese": "娥德丽恩 / 阿德丽",
    "pinyin": "é dé lì ēn / ā dé lì",
    "meaning": "beautiful, virtue, beautiful kindness / a, virtue, beautiful"
  },
  "Aelijah": {
    "chinese": "意来嘉",
    "pinyin": "yì lái jiā",
    "meaning": "intent, arrive, auspicious"
  },
  "Aevie": {
    "chinese": "爱碧",
    "pinyin": "ài bì",
    "meaning": "love, treasure"
  },
  "Aglorya": {
    "chinese": "阿格罗丽雅",
    "pinyin": "ā gé luó lì yǎ",
    "meaning": "standard, net, beauty, elegance"
  },
  "Agrifyna": {
    "chinese": "阿格丽菲娜",
    "pinyin": "ā gé lì fēi nà",
    "meaning": "standard beauty, fragrant elegance"
  },
  "Agustina": {
    "chinese": "阿古丝蒂娜 / 阿古丝",
    "pinyin": "ā gǔ sī dì nà / ā gǔ sī",
    "meaning": "a + luck, silk, flower stem, graceful / a + lucky, silk"
  },
  "Aiah": {
    "chinese": "爱雅",
    "pinyin": "ài yǎ",
    "meaning": "love elegance"
  },
  "Aidan": {
    "chinese": "爱旦",
    "pinyin": "ài dàn",
    "meaning": "love, dawn"
  },
  "Aiko": {
    "chinese": "爱劶",
    "pinyin": "ài zhǐ",
    "meaning": "love strives"
  },
  "Ailee": {
    "chinese": "爱丽",
    "pinyin": "aì lì",
    "meaning": "love beautiful"
  },
  "Ailyn": {
    "chinese": "爱琳",
    "pinyin": "ài lín",
    "meaning": "love gem"
  },
  "Aima": {
    "chinese": "爱玛",
    "pinyin": "ài mǎ",
    "meaning": "love, agate"
  },
  "Aira": {
    "chinese": "爱拉",
    "pinyin": "ài lā",
    "meaning": "love pull"
  },
  "Airena": {
    "chinese": "爱蕾娜",
    "pinyin": "ài lèi nà",
    "meaning": "love, bud, graceful"
  },
  "Airy": {
    "chinese": "爱丽",
    "pinyin": "ài lì",
    "meaning": "love beauty"
  },
  "Aisha": {
    "chinese": "爱莎",
    "pinyin": "ài shā",
    "meaning": "love, sedge grass/fern"
  },
  "Akira": {
    "chinese": "阿琪拉",
    "pinyin": "ā qí lā",
    "meaning": "a, fine jade, pull"
  },
  "Alana": {
    "chinese": "阿蕾娜",
    "pinyin": "ā lěi nà",
    "meaning": "a + flower bud, graceful"
  },
  "Aleigh": {
    "chinese": "阿丽",
    "pinyin": "ā lì",
    "meaning": "a + beautiful"
  },
  "Alejandra": {
    "chinese": "阿楽寒德拉",
    "pinyin": "ā lè hàn dé lā",
    "meaning": "a + happy, winter/cold, virtue, pull"
  },
  "Alessi": {
    "chinese": "阿楽希",
    "pinyin": "ā lè xī",
    "meaning": "a + happiness, hope"
  },
  "Alessia": {
    "chinese": "阿楽丝雅",
    "pinyin": "ā lè sī yǎ",
    "meaning": "a + happiness, silk, elegance"
  },
  "Alex": {
    "chinese": "阿楽克丝",
    "pinyin": "ā lè kè sī",
    "meaning": "happy, overcome, silk"
  },
  "Alexa": {
    "chinese": "阿楽克希雅",
    "pinyin": "ā lè kè xī yǎ",
    "meaning": "happy, overcome, hope, elegance"
  },
  "Alexis": {
    "chinese": "阿楽克希丝",
    "pinyin": "ā lè kè xī sī",
    "meaning": "a + happiness, overcome, hope, silk"
  },
  "Alfea": {
    "chinese": "阿露菲雅",
    "pinyin": "ā lù fēi yǎ",
    "meaning": "dew + fragrant + elegance"
  },
  "Alffania": {
    "chinese": "尔筏霓雅",
    "pinyin": "ěr fá ní yǎ",
    "meaning": "you (classical), raft, rainbow, elegance"
  },
  "Aliah": {
    "chinese": "阿丽雅",
    "pinyin": "ā lì yǎ",
    "meaning": "beautiful elegance"
  },
  "Alice": {
    "chinese": "爱丽丝",
    "pinyin": "ài lì sī",
    "meaning": "love, beautiful silk"
  },
  "Alisha": {
    "chinese": "阿丽霞",
    "pinyin": "ā lì xiá",
    "meaning": "a + beautiful, sunset/rosy sky"
  },
  "Allison": {
    "chinese": "阿丽森",
    "pinyin": "ā lì sēn",
    "meaning": "a + beautiful + forest"
  },
  "Allure": {
    "chinese": "阿露尔",
    "pinyin": "ā lù ěr",
    "meaning": "a + dew + you (classical)"
  },
  "Alma": {
    "chinese": "阿尔玛",
    "pinyin": "ā ěr mǎ",
    "meaning": "a, you (classical), agate"
  },
  "Aluby": {
    "chinese": "阿露碧",
    "pinyin": "ā lù bì",
    "meaning": "dew jade"
  },
  "Aluna": {
    "chinese": "阿露娜",
    "pinyin": "ā lù nà",
    "meaning": "graceful dew"
  },
  "Alya": {
    "chinese": "阿丽雅",
    "pinyin": "ā lì yǎ",
    "meaning": "beautiful elegance"
  },
  "Alyanna": {
    "chinese": "阿丽雅娜",
    "pinyin": "ā lì yǎ nà",
    "meaning": "beautiful, elegant, graceful"
  },
  "Alyrianna": {
    "chinese": "阿丽日安娜",
    "pinyin": "ā lì rì ān nà",
    "meaning": "a, beautiful, sun, peace, graceful"
  },
  "Amalthea": {
    "chinese": "娥玛尔蒂雅",
    "pinyin": "é mǎ ěr dì yǎ",
    "meaning": "beautiful, agate, you (classical) flower stem, elegance"
  },
  "Amaranthe": {
    "chinese": "阿玛尔燃特",
    "pinyin": "ā mǎ ěr rán tè",
    "meaning": "a + agate + you (classical) + ignite, special"
  },
  "Amaris": {
    "chinese": "阿玛丽丝",
    "pinyin": "ā mǎ lì sī",
    "meaning": "a + agate, beautiful, silk"
  },
  "Amaryllis": {
    "chinese": "阿玛瑞丽丝",
    "pinyin": "ā mǎ ruì lì sī",
    "meaning": "a + agate + auspicious beautiful silk"
  },
  "Ambay": {
    "chinese": "安贝",
    "pinyin": "ān bèi",
    "meaning": "peaceful treasure"
  },
  "Amelia": {
    "chinese": "阿梅丽雅",
    "pinyin": "ā méi lì yǎ",
    "meaning": "beautiful elegant plum flower"
  },
  "Amelie": {
    "chinese": "阿美丽",
    "pinyin": "ā měi lì",
    "meaning": "a + beautiful beauty"
  },
  "Ami": {
    "chinese": "爱蜜",
    "pinyin": "ài mì",
    "meaning": "love, honey"
  },
  "Amiee": {
    "chinese": "阿蜜",
    "pinyin": "ā mì",
    "meaning": "a + honey"
  },
  "Amielle": {
    "chinese": "阿蜜尔",
    "pinyin": "ā mì ěr",
    "meaning": "honey you (classical)"
  },
  "Amira": {
    "chinese": "阿蜜拉",
    "pinyin": "ā mì lā",
    "meaning": "pull honey"
  },
  "Amisha": {
    "chinese": "爱蜜霞",
    "pinyin": "aì mì xiá",
    "meaning": "love honey sunset/rose-colored sky"
  },
  "Ammara": {
    "chinese": "阿玛拉",
    "pinyin": "ā má lā",
    "meaning": "agate pulls"
  },
  "Amrita": {
    "chinese": "阿暮黎达",
    "pinyin": "ā mù lí dá",
    "meaning": "sunset, dark (Zayne's li), reach"
  },
  "Amy": {
    "chinese": "爱蜜",
    "pinyin": "aì mì",
    "meaning": "love honey"
  },
  "Amy Lizzy": {
    "chinese": "爱蜜 丽丝",
    "pinyin": "ài mì lì sī",
    "meaning": "love honey beautiful silk"
  },
  "Ana": {
    "chinese": "阿娜",
    "pinyin": "ā nà",
    "meaning": "graceful"
  },
  "Ana Valeria": {
    "chinese": "阿娜 / 芭楽丽雅",
    "pinyin": "ā nà / bà lè lì yǎ",
    "meaning": "a + graceful / fragrant plant, happy, beautiful, elegant"
  },
  "Anais": {
    "chinese": "阿柰意思",
    "pinyin": "ā nài yì sī",
    "meaning": "a + crabapple + meaning"
  },
  "Anati": {
    "chinese": "安娜蒂",
    "pinyin": "ān nà dì",
    "meaning": "peace, grace, stem (flower)"
  },
  "Andrea": {
    "chinese": "安德丽雅",
    "pinyin": "ān dé lì yǎ",
    "meaning": "peaceful virtue, beautiful elegance"
  },
  "Andréa": {
    "chinese": "安德蕾雅",
    "pinyin": "ān dé lěi yǎ",
    "meaning": "peace, virtue, flower bud, elegance"
  },
  "Andy": {
    "chinese": "安蒂",
    "pinyin": "ān dì",
    "meaning": "peaceful stem (flower)"
  },
  "Angela": {
    "chinese": "安杰拉",
    "pinyin": "ān jié lā",
    "meaning": "peace, heroic, pull"
  },
  "Angelica": {
    "chinese": "恩嘉黎卡",
    "pinyin": "ēn jiā lí kǎ",
    "meaning": "kindness, auspiciousness, dark (zayne's li), ka"
  },
  "Angeline": {
    "chinese": "恩嘉琳",
    "pinyin": "én jiā lín",
    "meaning": "kind, auspicious, the sound of gems"
  },
  "Angelita": {
    "chinese": "安玖丽塔",
    "pinyin": "ān jiǔ lì tǎ",
    "meaning": "peace, dark jade, beautiful, pagoda"
  },
  "Angie": {
    "chinese": "安吉",
    "pinyin": "ān jí",
    "meaning": "peace, luck"
  },
  "Anisey": {
    "chinese": "安意希",
    "pinyin": "ān yì xī",
    "meaning": "peace, intent, hope"
  },
  "Anju": {
    "chinese": "安珠",
    "pinyin": "ān zhū",
    "meaning": "peaceful pearl"
  },
  "Ann": {
    "chinese": "安",
    "pinyin": "ān",
    "meaning": "peace"
  },
  "Anna": {
    "chinese": "安娜",
    "pinyin": "ān nà",
    "meaning": "peaceful grace"
  },
  "Anne": {
    "chinese": "安",
    "pinyin": "ān",
    "meaning": "peace"
  },
  "Annette": {
    "chinese": "安讷特",
    "pinyin": "ān nè tè",
    "meaning": "peace, na, special"
  },
  "Annicka": {
    "chinese": "安霓卡",
    "pinyin": "ān ní kǎ",
    "meaning": "peaceful, rainbow + ka"
  },
  "Annie": {
    "chinese": "安霓",
    "pinyin": "ān ní",
    "meaning": "peace, rainbow"
  },
  "Apip": {
    "chinese": "阿碧谱",
    "pinyin": "ā bì pǔ",
    "meaning": "a + jade + music score"
  },
  "Aqila": {
    "chinese": "阿琦拉",
    "pinyin": "ā qí lā",
    "meaning": "a + precious jade + pull"
  },
  "Ara": {
    "chinese": "阿拉",
    "pinyin": "ā lā",
    "meaning": "pulls"
  },
  "Aracel": {
    "chinese": "阿拉璱尔",
    "pinyin": "ā lā sè ěr",
    "meaning": "a + pull, bright jade, you (classical)"
  },
  "Arcella Liu": {
    "chinese": "刘阿尔璱拉",
    "pinyin": "liú ā ěr sè lā",
    "meaning": "Liu + you (classical), bright jade, pull"
  },
  "Arctic": {
    "chinese": "阿尔克蒂克，北极",
    "pinyin": "ā ěr kè dì kè, běi jí",
    "meaning": "a + you (classical) + overcome + flower stem + overcome / Arctic translation"
  },
  "Arelya": {
    "chinese": "阿楽黎雅",
    "pinyin": "ā lè lí yǎ",
    "meaning": "happy, dark (Zayne's Li), elegance"
  },
  "Ari": {
    "chinese": "阿丽",
    "pinyin": "ā lì",
    "meaning": "beautiful"
  },
  "Aria": {
    "chinese": "爱丽雅",
    "pinyin": "ài lì yǎ",
    "meaning": "love beautiful elegance"
  },
  "Ariadne": {
    "chinese": "阿丽雅德恩",
    "pinyin": "ā lì yǎ dé ēn",
    "meaning": "a + beautiful, graceful, virtue, kindness"
  },
  "Arianne": {
    "chinese": "阿丽安",
    "pinyin": "ā lì ān",
    "meaning": "beautiful, peace"
  },
  "Arima": {
    "chinese": "阿丽玛",
    "pinyin": "ā lì mǎ",
    "meaning": "beautiful agate"
  },
  "Arin": {
    "chinese": "阿琳",
    "pinyin": "ā lín",
    "meaning": "the sound of gems"
  },
  "Arina": {
    "chinese": "阿丽娜",
    "pinyin": "ā lì nà",
    "meaning": "a + beautiful, graceful"
  },
  "Arisu": {
    "chinese": "阿丽苏",
    "pinyin": "ā lì sū",
    "meaning": "a + beautiful + revival"
  },
  "Arranea": {
    "chinese": "阿燃内雅",
    "pinyin": "ā rǎn nèi yǎ",
    "meaning": "ignite inner elegance"
  },
  "Arsea": {
    "chinese": "阿尔丝雅",
    "pinyin": "ā ěr sī yǎ",
    "meaning": "a + you (classical) + silk + elegance"
  },
  "Artemis": {
    "chinese": "阿尔忒弥斯",
    "pinyin": "ā ěr tè mí sī",
    "meaning": "official translit: a + unique + fill + this"
  },
  "Arwen": {
    "chinese": "阿尔雯",
    "pinyin": "ā ěr wén",
    "meaning": "you (classical), colorful clouds"
  },
  "Ash": {
    "chinese": "阿使 / 阿诗",
    "pinyin": "ā shǐ / ā shī",
    "meaning": "a + can use (best pronunciation); a + poem"
  },
  "Asha": {
    "chinese": "阿莎 / 阿霞",
    "pinyin": "ā shā / ā xiá",
    "meaning": "a + sedge grass/fern / a + sunset/rosy sky"
  },
  "Ashley": {
    "chinese": "阿诗蕾",
    "pinyin": "ā shī lèi",
    "meaning": "a + poem, flower bud"
  },
  "Asnu": {
    "chinese": "阿苏努",
    "pinyin": "ā sū nǔ",
    "meaning": "a + revival + effort"
  },
  "Aster": {
    "chinese": "阿丝特尔",
    "pinyin": "ā sī tè ěr",
    "meaning": "a + silk, special, you (classical)"
  },
  "Asteria": {
    "chinese": "阿丝特丽雅",
    "pinyin": "ā sī tè lì yǎ",
    "meaning": "silk, unique, beautiful, elegant"
  },
  "Astra": {
    "chinese": "阿斯塔",
    "pinyin": "ā sī tǎ",
    "meaning": "Infold's transliteration of Astra - this tower"
  },
  "Asumi": {
    "chinese": "阿苏蜜",
    "pinyin": "ā sū mì",
    "meaning": "a + revive, honey"
  },
  "Athanasia": {
    "chinese": "阿潭希雅",
    "pinyin": "ā tán xī yǎ",
    "meaning": "a + pond + hope + elegance"
  },
  "Athena": {
    "chinese": "雅典娜",
    "pinyin": "yǎ diǎn nà",
    "meaning": "official transliteration - elegant ceremony, graceful"
  },
  "Atika": {
    "chinese": "阿缇卡",
    "pinyin": "ā tì kǎ",
    "meaning": "a + red/orange silk + ka (card)"
  },
  "Atta": {
    "chinese": "阿塔",
    "pinyin": "ā tǎ",
    "meaning": "pagoda"
  },
  "Audrey": {
    "chinese": "奥黛丽，奥德丽",
    "pinyin": "ào dài lì, ào dé lì",
    "meaning": "official transliteration: profound, dark eyebrow paint, beautiful; ours: profound, virtuous beauty"
  },
  "Aura": {
    "chinese": "奥拉",
    "pinyin": "aò lā",
    "meaning": "profound pull"
  },
  "Aurelia": {
    "chinese": "奥雷黎雅",
    "pinyin": "aò lěi lí yǎ",
    "meaning": "profound, buds (leaf/flower), Dark (Zayne's Li), elegance"
  },
  "Aurielle": {
    "chinese": "藕黎尔楽",
    "pinyin": "ǒu lí ěr lè",
    "meaning": "lotus, dark (Zayne's Li), you (classical), happy"
  },
  "Aurora": {
    "chinese": "奥柔拉",
    "pinyin": "ào róu lā",
    "meaning": "profound soft pull"
  },
  "Awa": {
    "chinese": "阿娃",
    "pinyin": "ā wá",
    "meaning": "baby/doll"
  },
  "Axelya": {
    "chinese": "阿克璱黎雅",
    "pinyin": "ā kè sè lí yǎ",
    "meaning": "overcome + bright jade + dark (Zayne's Li) + elegance"
  },
  "Aya": {
    "chinese": "爱雅",
    "pinyin": "ài yǎ",
    "meaning": "elegant love"
  },
  "Ayame": {
    "chinese": "爱雅美",
    "pinyin": "ài yǎ měi",
    "meaning": "love elegant beauty"
  },
  "Ayara": {
    "chinese": "爱雅辣",
    "pinyin": "ài yǎ là",
    "meaning": "love elegant spice"
  },
  "Ayeisha": {
    "chinese": "爱意霞",
    "pinyin": "ài yì xiá",
    "meaning": "love, intent, sunset/rosy sky"
  },
  "Ayela": {
    "chinese": "爱拉，阿叶拉",
    "pinyin": "ài lā, ā yè lā",
    "meaning": "love pull, a + leaf, pull"
  },
  "Ayra": {
    "chinese": "阿丽雅",
    "pinyin": "ā lì yǎ",
    "meaning": "beautiful elegance"
  },
  "AyRin": {
    "chinese": "爱琳",
    "pinyin": "ài lín",
    "meaning": "love jade"
  },
  "Ayring": {
    "chinese": "爱玲",
    "pinyin": "ài líng",
    "meaning": "love, the sound of pendants"
  },
  "Ayu": {
    "chinese": "阿祐",
    "pinyin": "ā yòu",
    "meaning": "to bless or protect"
  },
  "Azae": {
    "chinese": "阿鰂",
    "pinyin": "ā zéi",
    "meaning": "a + cuttlefish (sorry, no other zay works)"
  },
  "Azahra": {
    "chinese": "阿柤拉",
    "pinyin": "ā zhā lā",
    "meaning": "a + hawthorn, pull"
  },
  "Azure": {
    "chinese": "阿珠儿 / 翠蓝",
    "pinyin": "ā zhū ér / cuì lán",
    "meaning": "pearl / azure"
  },
  "Basitha": {
    "chinese": "芭丝达",
    "pinyin": "bā sī dá",
    "meaning": "fragrant plant, silk, reach"
  },
  "Beatriz": {
    "chinese": "碧雅池丽丝",
    "pinyin": "bì yǎ chí lì sī",
    "meaning": "jade, elegance, pool, beautiful, silk"
  },
  "Bec": {
    "chinese": "贝卡",
    "pinyin": "bèi kǎ",
    "meaning": "precious + ka"
  },
  "Belén": {
    "chinese": "贝崚",
    "pinyin": "bèi léng",
    "meaning": "precious lofty (mountain)"
  },
  "Bella": {
    "chinese": "贝拉",
    "pinyin": "bèi là",
    "meaning": "precious pull"
  },
  "Bernadette": {
    "chinese": "贝尔娜德特",
    "pinyin": "bèi ěr nà dé tè",
    "meaning": "treasure, you (classical), graceful, virtue, special"
  },
  "Bianca": {
    "chinese": "碧安卡",
    "pinyin": "bì ān kǎ",
    "meaning": "jade + peace + ka"
  },
  "Bibin": {
    "chinese": "碧滨",
    "pinyin": "bì bīn",
    "meaning": "jade along the water's edge"
  },
  "Billie": {
    "chinese": "碧丽",
    "pinyin": "bì lì",
    "meaning": "jade, beautiful"
  },
  "Bina": {
    "chinese": "碧娜",
    "pinyin": "bì nà",
    "meaning": "jade + graceful"
  },
  "Blue": {
    "chinese": "捗露，蓝",
    "pinyin": "bù lù, lán",
    "meaning": "make progress + dew, blue (Translation)"
  },
  "Bree": {
    "chinese": "布丽",
    "pinyin": "bù lì",
    "meaning": "announce, beauty"
  },
  "Brena": {
    "chinese": "布楽娜",
    "pinyin": "bù lè nà",
    "meaning": "announce, happiness, graceful"
  },
  "Brenda": {
    "chinese": "布仁达",
    "pinyin": "bù rén dá",
    "meaning": "announce, kindness, reach"
  },
  "Bridgette": {
    "chinese": "布里吉特",
    "pinyin": "bù lǐ jí tè",
    "meaning": "official transliteration: announce, inside, lucky, unique"
  },
  "Brigitte": {
    "chinese": "布里吉特",
    "pinyin": "bù lǐ jí tè",
    "meaning": "official transliteration: announce, inside, lucky, special"
  },
  "Britney": {
    "chinese": "贝丽特妮",
    "pinyin": "bèi lì tè nī",
    "meaning": "precious beauty, unique girl"
  },
  "Brookie": {
    "chinese": "布露琪",
    "pinyin": "bù lù qí",
    "meaning": "announce dew fine jade"
  },
  "Bunga Itu Hitam": {
    "chinese": "帮尕意图和潭",
    "pinyin": "bāng gǎ yì tú hé tán",
    "meaning": "help small intention peaceful pond"
  },
  "Buni": {
    "chinese": "布霓",
    "pinyin": "bù ní",
    "meaning": "cloth, rainbow"
  },
  "Busra": {
    "chinese": "捗诗拉",
    "pinyin": "bù shī lā",
    "meaning": "make progress, poem, pull"
  },
  "Byul Annzerly": {
    "chinese": "碧尤尔 安泽尔丽",
    "pinyin": "bì yóu ěr ān zé ěr lì",
    "meaning": "jade, outstanding, you (classical), peace, lustrous, you (classical), beautiful"
  },
  "Caa": {
    "chinese": "茶",
    "pinyin": "chá",
    "meaning": "tea"
  },
  "Caelus": {
    "chinese": "凯维罗丝",
    "pinyin": "kǎi wèi luó sī",
    "meaning": "triumph maintains net silk"
  },
  "Cailey": {
    "chinese": "凯蕾",
    "pinyin": "kǎi lèi",
    "meaning": "triumphant flower bud"
  },
  "Cait": {
    "chinese": "凯特",
    "pinyin": "kǎi tè",
    "meaning": "triumphant, special"
  },
  "Caitlin": {
    "chinese": "凯特琳 / 凯特",
    "pinyin": "kǎi tè lín / kǎi tè",
    "meaning": "triumphant, special, gem / triumphant, special"
  },
  "Calafira": {
    "chinese": "卡拉菲拉",
    "pinyin": "kǎ lā fēi lā",
    "meaning": "ka + pull + fragrant + pull"
  },
  "Cali": {
    "chinese": "凯莉，可丽",
    "pinyin": "kǎi lì, kě lì",
    "meaning": "triumph jasmine, can be beautiful"
  },
  "Calista": {
    "chinese": "卡丽丝塔",
    "pinyin": "kǎ lì sī tǎ",
    "meaning": "ka + beautiful, silk, pagoda"
  },
  "Calistra": {
    "chinese": "卡丽丝特拉",
    "pinyin": "kǎ lì sī tè lā",
    "meaning": "ka + beautiful silk unique pull"
  },
  "Camille": {
    "chinese": "卡蜜尔",
    "pinyin": "kǎ mì ěr",
    "meaning": "ka + honey + you (classical)"
  },
  "Caoimhe": {
    "chinese": "葵华，葵芭",
    "pinyin": "kuí huá, kuí bā",
    "meaning": "sunflower, luxurious; sunflower, fragrant plant"
  },
  "Carelina": {
    "chinese": "卡热丽娜",
    "pinyin": "kǎ rè lì nà",
    "meaning": "ka + hot, beautiful, graceful"
  },
  "Carmen": {
    "chinese": "嘉𫞩",
    "pinyin": "jiā mén",
    "meaning": "auspicious red jade"
  },
  "Carmina": {
    "chinese": "卡尔敏娜",
    "pinyin": "kǎ ěr mǐn nà",
    "meaning": "ka + you (classical) + intelligent + graceful"
  },
  "Carolina": {
    "chinese": "卡柔丽娜",
    "pinyin": "kǎ róu lì nà",
    "meaning": "ka + soft + beautiful + graceful"
  },
  "Caroline": {
    "chinese": "卡柔来恩",
    "pinyin": "kǎ róu lái ēn",
    "meaning": "ka + soft + arrives + intent"
  },
  "Casey": {
    "chinese": "凯希",
    "pinyin": "kǎi xī",
    "meaning": "triumphant hope"
  },
  "Cassandra": {
    "chinese": "卡珊德拉，可善德拉",
    "pinyin": "kǎ shān dé lā, kě shàn dé lā",
    "meaning": "official translit: ka + coral + virtue + pull; ours: able, kindness, virtue, pull"
  },
  "Cata": {
    "chinese": "卡塔",
    "pinyin": "kǎ tǎ",
    "meaning": "ka + pagoda"
  },
  "Catherine": {
    "chinese": "卡特琳",
    "pinyin": "kǎ tè lín",
    "meaning": "ka + special, pearl"
  },
  "Cathleen": {
    "chinese": "凯璱琳",
    "pinyin": "kǎi sè lín",
    "meaning": "triumphant bright jade gem"
  },
  "Cecilia": {
    "chinese": "丝希丽雅",
    "pinyin": "sī xī lì yǎ",
    "meaning": "silk, hope, beauty, elegance"
  },
  "Celeste": {
    "chinese": "璱楽丝特",
    "pinyin": "sè lè sī tè",
    "meaning": "bright jade, happiness, silk, special"
  },
  "Celestia": {
    "chinese": "璱楽丝蒂雅",
    "pinyin": "sè lè sī dì yǎ",
    "meaning": "bright jade, happiness, silk, flower stem, elegance"
  },
  "Celestine": {
    "chinese": "璱丽丝婷",
    "pinyin": "sè lì sī tīng",
    "meaning": "bright jade, beautiful, silk, graceful"
  },
  "Cerise": {
    "chinese": "璱丽丝",
    "pinyin": "sè lì sī",
    "meaning": "bright jade, beautiful silk"
  },
  "Chante": {
    "chinese": "善特爱",
    "pinyin": "shàn tè ài",
    "meaning": "kindness, unique, love"
  },
  "Charlene": {
    "chinese": "霞尔琳",
    "pinyin": "xiā ér lín",
    "meaning": "sunset/rosy sky, you (classical), gem"
  },
  "Charlie": {
    "chinese": "姹尔丽，檫尔黎，杈尔力",
    "pinyin": "chà ěr lì, chá ěr lí, chā ěr lì",
    "meaning": "female: beautiful, you (classical), beautiful; gender-neutral: sassafras, you (classical), dark (Zayne's li); male: tree branch, you (classical), power/strength"
  },
  "Charlotte": {
    "chinese": "霞尔蕾特",
    "pinyin": "xiá ěr lèi tè",
    "meaning": "dew, you (classical), flower bud, special"
  },
  "Chaze": {
    "chinese": "切丝",
    "pinyin": "qiē sī",
    "meaning": "cut silk"
  },
  "Chelsea": {
    "chinese": "池尔希",
    "pinyin": "chí ěr xī",
    "meaning": "pool, you (classical), hope"
  },
  "Chess": {
    "chinese": "彻世",
    "pinyin": "chè shì",
    "meaning": "thorough (like Sylus's chè!) world"
  },
  "Chia": {
    "chinese": "琪雅",
    "pinyin": "qí yǎ",
    "meaning": "elegant fine jade"
  },
  "Chichi": {
    "chinese": "琪琦",
    "pinyin": "qí qí",
    "meaning": "fine, precious jade"
  },
  "Chidimma": {
    "chinese": "琦蒂玛",
    "pinyin": "qí dì mǎ",
    "meaning": "precious pearl, flower stem, agate"
  },
  "Chloe": {
    "chinese": "克搂意",
    "pinyin": "kè lǒu yì",
    "meaning": "overcome, embrace, intent"
  },
  "Christa": {
    "chinese": "克丽丝达",
    "pinyin": "kè lì sī dá",
    "meaning": "overcome, beauty, silk, reach"
  },
  "Christine": {
    "chinese": "克丽丝婷",
    "pinyin": "kè lì sī tīng",
    "meaning": "overcome + beauty + silk + graceful"
  },
  "Christy": {
    "chinese": "克丽丝缇",
    "pinyin": "kè lì sī tǐ",
    "meaning": "overcome, beautiful, silk, red-orange silk"
  },
  "Chrysant": {
    "chinese": "克丽善特",
    "pinyin": "kè lì shàn tè",
    "meaning": "overcome, beautiful, kind, special"
  },
  "Cinie": {
    "chinese": "丝霓",
    "pinyin": "sī ní",
    "meaning": "silk, rainbow"
  },
  "Cirah": {
    "chinese": "丝拉",
    "pinyin": "sī lā",
    "meaning": "silk pull"
  },
  "Claire": {
    "chinese": "克莱尔",
    "pinyin": "kè lái ěr",
    "meaning": "overcome, flower stem, you (classical)"
  },
  "Clementine": {
    "chinese": "克楽璊婷",
    "pinyin": "kè lè mén tíng",
    "meaning": "overcome, happiness, red jade, graceful"
  },
  "Clive": {
    "chinese": "克来步",
    "pinyin": "kè lái bù",
    "meaning": "overcome, arrive, step"
  },
  "Cole": {
    "chinese": "蔻楽",
    "pinyin": "kòu lè",
    "meaning": "cardamom happiness"
  },
  "Coline": {
    "chinese": "可琳",
    "pinyin": "kě lín",
    "meaning": "able + gem (ke sounds like kuh)"
  },
  "Connie": {
    "chinese": "慷妮",
    "pinyin": "kāng nī",
    "meaning": "ardent/generous + rainbow"
  },
  "Constanza": {
    "chinese": "慷丝潭洒",
    "pinyin": "kāng sī tán sǎ",
    "meaning": "ardent/generous + silk + pond + unrestrained/carefree"
  },
  "Cora": {
    "chinese": "蔻拉",
    "pinyin": "kòu lā",
    "meaning": "cardamom, pull"
  },
  "Cortney": {
    "chinese": "克藕尔特霓",
    "pinyin": "kè ǒu ěr tè ní",
    "meaning": "overcome, lotus root, special, rainbow"
  },
  "Corynn": {
    "chinese": "克琳",
    "pinyin": "kè lín",
    "meaning": "overcome gem"
  },
  "Courtney": {
    "chinese": "柯特妮",
    "pinyin": "kē tè nī",
    "meaning": "branch/stalk + unique + girl"
  },
  "Crizel": {
    "chinese": "克丽吉尔",
    "pinyin": "kè lì jí ěr",
    "meaning": "overcome, beautiful, lucky, you (classical)"
  },
  "Cross": {
    "chinese": "克柔丝",
    "pinyin": "kè róu sī",
    "meaning": "overcome, soft, silk"
  },
  "Cryla": {
    "chinese": "克丽拉",
    "pinyin": "kè lì lā",
    "meaning": "overcome, beautiful, pull"
  },
  "Crystal": {
    "chinese": "克丽丝朵",
    "pinyin": "kè lì sī duǒ",
    "meaning": "overcome beautiful silk flower"
  },
  "Cyntia": {
    "chinese": "心蒂雅",
    "pinyin": "xīn dì yǎ",
    "meaning": "heart + flower stem + elegance"
  },
  "Dana": {
    "chinese": "达娜",
    "pinyin": "dá nà",
    "meaning": "reach, graceful"
  },
  "Dane": {
    "chinese": "德恩",
    "pinyin": "dé ēn",
    "meaning": "virtuous kindness"
  },
  "Dani": {
    "chinese": "达霓",
    "pinyin": "dá ní",
    "meaning": "reach, rainbow"
  },
  "Dania": {
    "chinese": "炟妮雅",
    "pinyin": "dá nī yǎ",
    "meaning": "da + beautiful girl"
  },
  "Danya": {
    "chinese": "旦雅",
    "pinyin": "dān yǎ",
    "meaning": "elegant dawn"
  },
  "Dara": {
    "chinese": "达拉",
    "pinyin": "dá lā",
    "meaning": "reach + pull"
  },
  "Daraporn": {
    "chinese": "达拉泼尔恩",
    "pinyin": "dá lā pō ěr ēn",
    "meaning": "reach + pull + splash + you (classical) + thought"
  },
  "Dareen": {
    "chinese": "达琳",
    "pinyin": "dá lín",
    "meaning": "reach gem"
  },
  "Darling": {
    "chinese": "达尔琳",
    "pinyin": "dá ěr lín",
    "meaning": "reach, you (classical), gem"
  },
  "Dasom": {
    "chinese": "达宋",
    "pinyin": "dá sòng",
    "meaning": "reach + Song dynasty"
  },
  "Daynie": {
    "chinese": "德恩妮",
    "pinyin": "dé ēn nī",
    "meaning": "virtuous kind girl"
  },
  "Dei": {
    "chinese": "黛",
    "pinyin": "dài",
    "meaning": "This is as close as we can get to Dei"
  },
  "Delia": {
    "chinese": "德丽雅",
    "pinyin": "dé lì yǎ",
    "meaning": "virtue, beautiful, graceful"
  },
  "Delilah": {
    "chinese": "德来拉",
    "pinyin": "dé lái lā",
    "meaning": "virtue, arrives, pull"
  },
  "Denya": {
    "chinese": "德霓雅",
    "pinyin": "dé ní yǎ",
    "meaning": "virtue, rainbow, graceful"
  },
  "Dessa": {
    "chinese": "德洒",
    "pinyin": "dé sǎ",
    "meaning": "virtue, unrestrained/careless"
  },
  "Devyn": {
    "chinese": "德雯",
    "pinyin": "dé wén",
    "meaning": "virtuous colorful clouds"
  },
  "Dew": {
    "chinese": "笃；露",
    "pinyin": "dǔ ; lù",
    "meaning": "sincere; dew (translation)"
  },
  "Dhanika": {
    "chinese": "达霓卡",
    "pinyin": "dá ní kǎ",
    "meaning": "reach, rainbow, ka (card)"
  },
  "Dia": {
    "chinese": "蒂雅",
    "pinyin": "dì yǎ",
    "meaning": "flower stem, elegance"
  },
  "Dia Ryan": {
    "chinese": "蒂雅 / 来恩",
    "pinyin": "dì yǎ / lái ēn",
    "meaning": "flower stem + elegance / arrive + kindness"
  },
  "Dia-Ryan": {
    "chinese": "蒂雅来恩",
    "pinyin": "dì yǎ lái ēn",
    "meaning": "flower stem, elegance, arrive, kindness"
  },
  "Dian": {
    "chinese": "蒂安",
    "pinyin": "dì ān",
    "meaning": "flower stem, peace"
  },
  "Diana": {
    "chinese": "蒂安娜",
    "pinyin": "dì ān nà",
    "meaning": "flower stem, peace, graceful"
  },
  "Dina": {
    "chinese": "蒂娜",
    "pinyin": "dì nà",
    "meaning": "flower stem, graceful"
  },
  "Diva": {
    "chinese": "蒂芭",
    "pinyin": "dì bā",
    "meaning": "fragrant plant stem (flower/leaf)"
  },
  "Dominika": {
    "chinese": "斗敏霓卡 / 斗蜜",
    "pinyin": "dòu mǐn ní kǎ / dòu mì",
    "meaning": "Dipper (constellation)/fight + intelligent + rainbow + graceful"
  },
  "Donna": {
    "chinese": "达娜",
    "pinyin": "dá nà",
    "meaning": "reach + graceful"
  },
  "Dovah": {
    "chinese": "斗芭",
    "pinyin": "dòu bā",
    "meaning": "big dipper/fight, fragrant plant"
  },
  "Dretch": {
    "chinese": "蒂热赤",
    "pinyin": "dì rè chì",
    "meaning": "flower stem, heat, red"
  },
  "Eden": {
    "chinese": "意登",
    "pinyin": "yì dēng",
    "meaning": "intent + ascend"
  },
  "Edith": {
    "chinese": "爱蒂丝，意蒂特",
    "pinyin": "aì dì sī, yì dì tè",
    "meaning": "love stems silk, intent stem special"
  },
  "Eika": {
    "chinese": "爱卡",
    "pinyin": "ài kǎ",
    "meaning": "love, ka"
  },
  "Eina": {
    "chinese": "爱娜",
    "pinyin": "ài nà",
    "meaning": "love graceful"
  },
  "Eir Ayln": {
    "chinese": "尔爱琳",
    "pinyin": "ěr ài lín",
    "meaning": "you (classical), love, precious gem"
  },
  "Eirwyn": {
    "chinese": "爱尔维恩",
    "pinyin": "ài ěr wéi ēn",
    "meaning": "love, you (classical), maintain, kindness"
  },
  "Elara": {
    "chinese": "娥拉辣",
    "pinyin": "é lā là",
    "meaning": "beautiful, pull, spicy"
  },
  "Elena": {
    "chinese": "爱蕾娜，娥蕾娜",
    "pinyin": "ài lěi nà, é lěi nà",
    "meaning": "love, fragrant, graceful, beautiful bud graceful"
  },
  "Eli": {
    "chinese": "娥丽",
    "pinyin": "é lì",
    "meaning": "graceful, beautiful"
  },
  "Elise": {
    "chinese": "娥丽丝",
    "pinyin": "è lì sī",
    "meaning": "pretty girl, beautiful, silk"
  },
  "Eliza": {
    "chinese": "娥来杂",
    "pinyin": "é lái zá",
    "meaning": "beautiful + arrive + mixed"
  },
  "Elizabeth": {
    "chinese": "娥丽萨白",
    "pinyin": "é lì sā bái",
    "meaning": "pretty girl, beautiful bodhitsattva, white/pure"
  },
  "Ella": {
    "chinese": "爱拉，娥拉",
    "pinyin": "aì lā, é lā",
    "meaning": "love pulls, beautiful pull"
  },
  "Ellen": {
    "chinese": "娥仁",
    "pinyin": "é rén",
    "meaning": "beautiful, kind"
  },
  "Ellery": {
    "chinese": "娥楽丽",
    "pinyin": "é lè lì",
    "meaning": "beautiful, happiness, beauty"
  },
  "Ellie": {
    "chinese": "叶丽",
    "pinyin": "yè lì",
    "meaning": "beautiful leaf"
  },
  "Ellis": {
    "chinese": "娥丽丝",
    "pinyin": "é lì sī",
    "meaning": "graceful, beautiful, silk"
  },
  "Eloise": {
    "chinese": "娥镂意丝",
    "pinyin": "é lòu yì sī",
    "meaning": "beautiful, engrave, intent, silk"
  },
  "Elsa": {
    "chinese": "尔洒",
    "pinyin": "ěr sǎ",
    "meaning": "you (classical), unrestrained/carefree"
  },
  "Ember": {
    "chinese": "恩贝尔",
    "pinyin": "ēn bèi ěr",
    "meaning": "kind, precious, you (fclassical)"
  },
  "Emerald": {
    "chinese": "娥玛热德",
    "pinyin": "é mǎ rè dé",
    "meaning": "beautiful, agate, hot, virtue"
  },
  "Emilia": {
    "chinese": "娥蜜莉雅",
    "pinyin": "é mì lì yǎ",
    "meaning": "beautiful, honey, jasmine, elegance"
  },
  "Emma": {
    "chinese": "恩玛",
    "pinyin": "ēn mǎ",
    "meaning": "kind agate"
  },
  "Emmari": {
    "chinese": "娥玛丽",
    "pinyin": "é mǎ lì",
    "meaning": "beautiful, agate, beautiful"
  },
  "Empress Rogue Red": {
    "chinese": "赤红女皇",
    "pinyin": "chì hóng nǚ huáng",
    "meaning": "Crimson Empress"
  },
  "Emrys": {
    "chinese": "爱暮丽丝",
    "pinyin": "aì mù lì sī",
    "meaning": "love, sunset, beautiful, silk"
  },
  "Erica": {
    "chinese": "爱丽卡",
    "pinyin": "ài lì kǎ",
    "meaning": "love, beauty, ka (card)"
  },
  "Eril": {
    "chinese": "尔尤",
    "pinyin": "ěr yóu",
    "meaning": "you (classical), outstanding"
  },
  "Eshal": {
    "chinese": "意霞楽",
    "pinyin": "yì xiá lè",
    "meaning": "intention, sunset/rosy sky, happiness"
  },
  "Esther": {
    "chinese": "娥璱特",
    "pinyin": "é sè tè",
    "meaning": "beautiful bright jade, unique"
  },
  "Estheya": {
    "chinese": "阿丝缇雅",
    "pinyin": "ā sī tǐ yǎ",
    "meaning": "a + silk, special, graceful"
  },
  "Estibaliz": {
    "chinese": "娥丝蒂芭丽滋",
    "pinyin": "é sī dì bā lì zī",
    "meaning": "beautiful silk, flower stem, fragrant plant, beautiful, grow"
  },
  "Etheryna": {
    "chinese": "娥特琳娜",
    "pinyin": "é tè lín nà",
    "meaning": "beautiful, unique, gem, graceful"
  },
  "Eve": {
    "chinese": "意福",
    "pinyin": "yì fú",
    "meaning": "intent, fortune"
  },
  "Evelyn": {
    "chinese": "爱福琳",
    "pinyin": "ài fú lín",
    "meaning": "love + fortune + gem"
  },
  "Everett": {
    "chinese": "娥贝热特",
    "pinyin": "é bèi rè tè",
    "meaning": "beautiful, treasure, hot, special"
  },
  "Evren": {
    "chinese": "娥布仁",
    "pinyin": "é bù rén",
    "meaning": "beautiful, announce, kindness"
  },
  "Fadia": {
    "chinese": "茷蒂雅",
    "pinyin": "fá dì yǎ",
    "meaning": "fragrant plant, flower stem, elegance"
  },
  "Fairy": {
    "chinese": "仙女",
    "pinyin": "xiānnǚ",
    "meaning": "fairy (literal)"
  },
  "Fania": {
    "chinese": "筏霓雅",
    "pinyin": "fá ní yǎ",
    "meaning": "raft, rainbow, elegance"
  },
  "Farah": {
    "chinese": "茷拉",
    "pinyin": "fá lā",
    "meaning": "dense grass, pull"
  },
  "Fary": {
    "chinese": "茷丽",
    "pinyin": "fá lì",
    "meaning": "dense grass, beautiful"
  },
  "Fawn": {
    "chinese": "茷藕恩，茷恩，芳",
    "pinyin": "fá ǒu ēn, fá ēn, fāng",
    "meaning": "fragrant plant, lotus root, kindness; fragrant plant, kindness; fragrant"
  },
  "Faye": {
    "chinese": "菲",
    "pinyin": "fēi",
    "meaning": "lush and fragrant"
  },
  "Felicia": {
    "chinese": "菲丽丝雅",
    "pinyin": "fēi lì sī yǎ",
    "meaning": "fragrant, beauty, silk, elegance"
  },
  "Fern": {
    "chinese": "小蕨",
    "pinyin": "xiǎo jué",
    "meaning": "little fern (translation)"
  },
  "Fernanda": {
    "chinese": "菲尔南达 / 菲尔",
    "pinyin": "fēi ěr nán dá / fēi ěr",
    "meaning": "fragrant, you (classical) south, reach / fragrant, you (classical)"
  },
  "Fey": {
    "chinese": "菲",
    "pinyin": "fēi",
    "meaning": "lush and fragrant"
  },
  "Fia": {
    "chinese": "菲雅",
    "pinyin": "fēi yǎ",
    "meaning": "fragrant, elegant"
  },
  "Fien": {
    "chinese": "菲恩",
    "pinyin": "fēi ēn",
    "meaning": "fragrant kindness"
  },
  "Fifi": {
    "chinese": "菲菲",
    "pinyin": "fēi fēi",
    "meaning": "lush and fragrant"
  },
  "Fiona": {
    "chinese": "菲藕娜",
    "pinyin": "fēi ǒu nà",
    "meaning": "lush, lotus root, graceful"
  },
  "Fira": {
    "chinese": "菲拉",
    "pinyin": "fēi lā",
    "meaning": "fragrant pull"
  },
  "Flavie": {
    "chinese": "福拉碧",
    "pinyin": "fú lā bì",
    "meaning": "fortune, pull, jade"
  },
  "Fleur": {
    "chinese": "菲楽尔",
    "pinyin": "fēi lè ér",
    "meaning": "fragrant happy you (classical)"
  },
  "Flint-Emanda": {
    "chinese": "福琳特 - 娥曼达",
    "pinyin": "fú lín tè - é màn dá",
    "meaning": "fortune, gem, special - beautiful, graceful, reach"
  },
  "Flora": {
    "chinese": "菲罗雅",
    "pinyin": "fēi luó yǎ",
    "meaning": "fragrant, net, elegance"
  },
  "Florence": {
    "chinese": "菲罗仁丝",
    "pinyin": "fēi luó rén sī",
    "meaning": "fragrant + net + kind + silk"
  },
  "Florithea": {
    "chinese": "菲罗丽蒂雅",
    "pinyin": "fēi luó lì dì yǎ",
    "meaning": "lush, net, beautiful, flower stem, elegance"
  },
  "Francine": {
    "chinese": "福珃心",
    "pinyin": "fú rán xīn",
    "meaning": "fortune, jade, heart"
  },
  "Francy": {
    "chinese": "菲燃希",
    "pinyin": "fēi rán xī",
    "meaning": "fragrant, ignite, hope"
  },
  "Freya": {
    "chinese": "惠雅，菲雅",
    "pinyin": "huì yǎ, fēi yǎ",
    "meaning": "kind elegance; fragrant, graceful"
  },
  "Freyana": {
    "chinese": "菲楽雅娜",
    "pinyin": "fēi lè yǎ nà",
    "meaning": "fragrant, happiness, elegance, graceful"
  },
  "Gabi": {
    "chinese": "尕碧",
    "pinyin": "gǎ bì",
    "meaning": "little jade"
  },
  "Gabija": {
    "chinese": "尕碧雅",
    "pinyin": "gǎ bì yǎ",
    "meaning": "little, jade, elegance"
  },
  "Gabriela": {
    "chinese": "加布里艾拉，尕布黎雅",
    "pinyin": "jiā bù lǐ ài lā, gǎ bù lí yǎ",
    "meaning": "official transliteration (meaningless); ours: little + bu + Dark (Zayne's Li), elegance"
  },
  "Gaby": {
    "chinese": "嘉碧",
    "pinyin": "jiā bì",
    "meaning": "auspicious jade"
  },
  "Gale": {
    "chinese": "给尔",
    "pinyin": "gěi ěr",
    "meaning": "Give (to) you"
  },
  "Garu": {
    "chinese": "凯露",
    "pinyin": "kaǐ lù",
    "meaning": "Triumph dew - there is no translation of Garu"
  },
  "Gel": {
    "chinese": "杰楽",
    "pinyin": "jié lè",
    "meaning": "heroic happiness"
  },
  "Gemma": {
    "chinese": "杰玛",
    "pinyin": "jié mǎ",
    "meaning": "heroic agate"
  },
  "Genesis": {
    "chinese": "杰讷诗丝",
    "pinyin": "jié nè shī sī",
    "meaning": "heroic, na, poem, silk"
  },
  "Genie": {
    "chinese": "吉霓",
    "pinyin": "jí ní",
    "meaning": "lucky, rainbow"
  },
  "Georgina": {
    "chinese": "吉藕尔吉娜",
    "pinyin": "jí ǒu ěr jí nà",
    "meaning": "lucky, lotus root, you (classical), lucky, graceful"
  },
  "Gigi": {
    "chinese": "吉吉",
    "pinyin": "jí jí",
    "meaning": "lucky lucky"
  },
  "Giselle": {
    "chinese": "吉泽尔",
    "pinyin": "jí zé ěr",
    "meaning": "lucky, luster, you (classical)"
  },
  "Gladise": {
    "chinese": "格拉蒂丝",
    "pinyin": "gé lā dì sī",
    "meaning": "standard, pull, flower stem, silk"
  },
  "Glorii": {
    "chinese": "格罗丽",
    "pinyin": "gé luó lì",
    "meaning": "standard, net, beautiful"
  },
  "Grace": {
    "chinese": "格蕾丝",
    "pinyin": "gé lèi sī",
    "meaning": "standard, buds (leaf/flower), silk"
  },
  "Gracy": {
    "chinese": "格蕾喜",
    "pinyin": "gé lěi xī",
    "meaning": "standard buds (tree/flower buds) happiness"
  },
  "Greta Raison": {
    "chinese": "格蕾塔 / 蕾森",
    "pinyin": "gé lèi tǎ / lěi sēn",
    "meaning": "standard, flower buds, pagoda / flower bud forest"
  },
  "Grimoire": {
    "chinese": "格里魔尔",
    "pinyin": "gé lǐ mō ér",
    "meaning": "standard transliteration: means standard Grimoire phonetically. Characters used: standard, inside, demon, you (formal archaic)"
  },
  "Gwen": {
    "chinese": "格雯",
    "pinyin": "gé wén",
    "meaning": "standard multicolored clouds"
  },
  "Haley": {
    "chinese": "黑丽",
    "pinyin": "hēi lì",
    "meaning": "black, beautiful"
  },
  "Hana": {
    "chinese": "哈娜",
    "pinyin": "hā nà",
    "meaning": "ha + graceful"
  },
  "Hana Lu": {
    "chinese": "露哈娜",
    "pinyin": "lù hā nà",
    "meaning": "dew + ha + graceful"
  },
  "Hanayuki": {
    "chinese": "哈娜玉琪",
    "pinyin": "hā nà yù qí",
    "meaning": "graceful fine jade"
  },
  "Hani": {
    "chinese": "哈霓",
    "pinyin": "hā ní",
    "meaning": "ha + rainbow"
  },
  "Hanieh": {
    "chinese": "哈霓娥",
    "pinyin": "hā ní é",
    "meaning": "ha + rainbow + beautiful"
  },
  "Hanna": {
    "chinese": "哈娜",
    "pinyin": "hā nà",
    "meaning": "graceful"
  },
  "Hanna Nadia": {
    "chinese": "哈娜 娜蒂雅",
    "pinyin": "hā nà nà dì yǎ",
    "meaning": "ha + graceful - graceful, flower stem, elegance"
  },
  "Hannah": {
    "chinese": "寒娜",
    "pinyin": "hán nà",
    "meaning": "cold/winter, graceful"
  },
  "Hannan": {
    "chinese": "寒南",
    "pinyin": "hán nán",
    "meaning": "cold/winter, south"
  },
  "Hanni": {
    "chinese": "寒霓",
    "pinyin": "hán ní",
    "meaning": "winter/cold, rainbow"
  },
  "Hansa": {
    "chinese": "寒洒",
    "pinyin": "hán sǎ",
    "meaning": "cold/winter + carefree/unrestrained"
  },
  "Hart": {
    "chinese": "哈尔特",
    "pinyin": "hā ěr tè",
    "meaning": "ha + you (classical) + unique"
  },
  "Haru": {
    "chinese": "哈缛",
    "pinyin": "hā rù",
    "meaning": "ha + beautiful"
  },
  "Haruki": {
    "chinese": "哈缛琪 / 春树",
    "pinyin": "hā rù qí / chūn shù",
    "meaning": "ha + beautiful, fine jade / spring tree"
  },
  "Haven": {
    "chinese": "黑奔",
    "pinyin": "hēi bēn",
    "meaning": "black, soaring/galloping"
  },
  "Hayley": {
    "chinese": "黑黎",
    "pinyin": "hēi lí",
    "meaning": "black darkness (Zayne's Li)"
  },
  "Heather": {
    "chinese": "赫泽",
    "pinyin": "hè zé",
    "meaning": "awe-inspiring luster"
  },
  "Helen Lee": {
    "chinese": "黎 河仁",
    "pinyin": "lí hé rén",
    "meaning": "Dark (Zayne's Li) + river + kind"
  },
  "Helena": {
    "chinese": "河蕾娜",
    "pinyin": "hé lěi nà",
    "meaning": "river, flower bud, graceful"
  },
  "Hera": {
    "chinese": "河拉",
    "pinyin": "hé lā",
    "meaning": "river, pull"
  },
  "Heylon": {
    "chinese": "黑龙",
    "pinyin": "hēi lóng",
    "meaning": "black dragon :D"
  },
  "Hikari": {
    "chinese": "和卡丽",
    "pinyin": "hé kǎ lì",
    "meaning": "peace + ka + beauty"
  },
  "Holly": {
    "chinese": "哈丽",
    "pinyin": "hā lì",
    "meaning": "ha + beauty"
  },
  "Honey": {
    "chinese": "寒霓",
    "pinyin": "hán ní",
    "meaning": "winter/cold + rainbow"
  },
  "Hope": {
    "chinese": "后瀑",
    "pinyin": "hòu pù",
    "meaning": "empress waterfall"
  },
  "Houseki": {
    "chinese": "后璱琦",
    "pinyin": "hòu sè qí",
    "meaning": "Empress, bright jade, precious jade"
  },
  "Hyera": {
    "chinese": "海娥拉",
    "pinyin": "hǎi é lā",
    "meaning": "ocean, beautiful girl, pulls"
  },
  "Icarus": {
    "chinese": "意卡黎丝",
    "pinyin": "yì kǎ lí sī",
    "meaning": "intent + ka + Dark (Zayne's Li), silk"
  },
  "Ida": {
    "chinese": "爱达",
    "pinyin": "ài dá",
    "meaning": "love, reach"
  },
  "Iman": {
    "chinese": "意曼",
    "pinyin": "yì màn",
    "meaning": "intent, graceful"
  },
  "ioana": {
    "chinese": "爱婉娜",
    "pinyin": "ài wǎn nà",
    "meaning": "love, graceful, elegant"
  },
  "Iqra": {
    "chinese": "意克拉",
    "pinyin": "yì kè lā",
    "meaning": "intent, overcome, pull"
  },
  "Irene": {
    "chinese": "爱琳",
    "pinyin": "ài lín",
    "meaning": "love gem"
  },
  "Irish": {
    "chinese": "爱丽诗",
    "pinyin": "ài lì shī",
    "meaning": "love beautiful poem"
  },
  "Iroha": {
    "chinese": "意柔哈",
    "pinyin": "yì róu hā",
    "meaning": "intent, soft + ha"
  },
  "Isa": {
    "chinese": "爱杂，意洒",
    "pinyin": "ài zá, yì sǎ",
    "meaning": "love, mixed; intent, carefree"
  },
  "Isabella": {
    "chinese": "伊莎贝拉",
    "pinyin": "yī shā bèi lā",
    "meaning": "official transliteration: yi + sedge grass/fern + precious + pull"
  },
  "Isabeth": {
    "chinese": "意洒贝特",
    "pinyin": "yì sǎ bèi tè",
    "meaning": "intent, carefree, treasure, special"
  },
  "Ishika": {
    "chinese": "意希卡",
    "pinyin": "yì xī kǎ",
    "meaning": "intent, hope, ka (card)"
  },
  "Isola": {
    "chinese": "意锼拉",
    "pinyin": "yì sōu lā",
    "meaning": "intent, engrave, pull"
  },
  "Isra": {
    "chinese": "意诗拉",
    "pinyin": "yì shī lā",
    "meaning": "intent, special, pull"
  },
  "Iu": {
    "chinese": "爱玉",
    "pinyin": "ài yù",
    "meaning": "love jade"
  },
  "Ivory": {
    "chinese": "爱博丽",
    "pinyin": "ài bó lì",
    "meaning": "love, abundant, beautiful"
  },
  "Ivy": {
    "chinese": "爱碧",
    "pinyin": "ài bì",
    "meaning": "love, jade"
  },
  "Izzati": {
    "chinese": "意柤缇",
    "pinyin": "yì zhā tì",
    "meaning": "intent, hawthorne, orange/red silk"
 },
  "Izzie": {
    "chinese": "意滋",
    "pinyin": "yì zī",
    "meaning": "intent, grow"
  },
  "Jackie": {
    "chinese": "杰琪",
    "pinyin": "jié qí",
    "meaning": "heroic + fine jade"
  },
  "Jade": {
    "chinese": "杰德",
    "pinyin": "jié dé",
    "meaning": "heroic virtue"
  },
  "Jam": {
    "chinese": "杰暮",
    "pinyin": "jié mù",
    "meaning": "heroic sunset"
  },
  "Jamie": {
    "chinese": "杰蜜",
    "pinyin": "jié mì",
    "meaning": "heroic + honey"
  },
  "Janan": {
    "chinese": "嘉南",
    "pinyin": "jiā nán",
    "meaning": "auspicious south"
  },
  "Jane": {
    "chinese": "嘉恩",
    "pinyin": "jiā ēn",
    "meaning": "auspicious kindness"
  },
  "Janell": {
    "chinese": "嘉呢楽",
    "pinyin": "jiā ne lè",
    "meaning": "auspicious + ne + happiness"
  },
  "Jani": {
    "chinese": "嘉妮",
    "pinyin": "jiā nī",
    "meaning": "auspicious girl"
  },
  "Janna": {
    "chinese": "嘉娜",
    "pinyin": "jiā nà",
    "meaning": "auspicious elegance"
  },
  "Jasmine": {
    "chinese": "N/A",
    "pinyin": "n/a",
    "meaning": ""
  },
  "Jayden": {
    "chinese": "杰登",
    "pinyin": "jié dēng",
    "meaning": "Heroic ascension"
  },
  "Jayenne": {
    "chinese": "杰恩",
    "pinyin": "jié ēn",
    "meaning": "heroic kindness"
  },
  "Jaylene": {
    "chinese": "杰琳",
    "pinyin": "jié lín",
    "meaning": "heroic gem"
  },
  "Jazmin": {
    "chinese": "嘉丝敏",
    "pinyin": "jiā sī mǐn",
    "meaning": "auspicious, silk, intelligent"
  },
  "Jazzy": {
    "chinese": "杰喜",
    "pinyin": "jié xǐ",
    "meaning": "heroic happiness"
  },
  "Jenn": {
    "chinese": "珍",
    "pinyin": "zhēn",
    "meaning": "Precious"
  },
  "Jenna": {
    "chinese": "杰娜",
    "pinyin": "jié nà",
    "meaning": "heroic, graceful"
  },
  "Jennie": {
    "chinese": "珍妮",
    "pinyin": "zhēn nī",
    "meaning": "treasure girl"
  },
  "Jennifer": {
    "chinese": "珍妮弗",
    "pinyin": "zhēn nī fú",
    "meaning": "official transliteration, means precious, girl, fu (for fer)"
  },
  "Jennini": {
    "chinese": "珍霓妮",
    "pinyin": "zhěn ní nī",
    "meaning": "precious rainbow girl"
  },
  "Jenny": {
    "chinese": "珍妮",
    "pinyin": "zhēnnī",
    "meaning": "Precious girl"
  },
  "Jeralyn": {
    "chinese": "杰拉琳",
    "pinyin": "jié lā lín",
    "meaning": "heroic, pull, forest"
  },
  "Jerene": {
    "chinese": "杰琳",
    "pinyin": "jié lín",
    "meaning": "heroic gem"
  },
  "Jescel": {
    "chinese": "杰璱尔",
    "pinyin": "jié sè ěr",
    "meaning": "heroic, bright jade, you (classical)"
  },
  "Jessica": {
    "chinese": "杰希卡",
    "pinyin": "jié xī kǎ",
    "meaning": "heroic, hope, ka"
  },
  "Jessie": {
    "chinese": "杰希",
    "pinyin": "jié xī",
    "meaning": "heroic, hope"
  },
  "Jewel": {
    "chinese": "玖雾尔",
    "pinyin": "jiǔ wù ěr",
    "meaning": "black jade, mist, you (classical)"
  },
  "Jeya": {
    "chinese": "杰雅",
    "pinyin": "jié yǎ",
    "meaning": "heroic elegance"
  },
  "Ji-cha": {
    "chinese": "吉茶",
    "pinyin": "jí chá",
    "meaning": "heroic, tea"
  },
  "Jia": {
    "chinese": "吉雅",
    "pinyin": "jí yǎ",
    "meaning": "lucky elegance"
  },
  "Jihan": {
    "chinese": "吉澣",
    "pinyin": "jí hàn",
    "meaning": "lucky vastness"
  },
  "Jinnie": {
    "chinese": "金妮",
    "pinyin": "jīn nī",
    "meaning": "gold girl"
  },
  "Joeline": {
    "chinese": "玖琳",
    "pinyin": "jiǔ lín",
    "meaning": "black jade gem"
  },
  "Joelle": {
    "chinese": "玖尔楽",
    "pinyin": "jiǔ ěr lè",
    "meaning": "black jade, you, happiness"
  },
  "Johanna": {
    "chinese": "玖安娜",
    "pinyin": "jiǔ ān nà",
    "meaning": "black jade, peace, graceful"
  },
  "Jolie": {
    "chinese": "玖丽",
    "pinyin": "jiǔ lì",
    "meaning": "black jade, beautiful"
  },
  "Jordan": {
    "chinese": "玖藕尔登",
    "pinyin": "jiǔ ǒu ěr dēng",
    "meaning": "black jade, lotus root, you (classical), ascend"
  },
  "Josephine": {
    "chinese": "玖璱菲恩",
    "pinyin": "jiǔ sè fēi ēn",
    "meaning": "black jade, bright jade, fragrant, kindness"
  },
  "Joy": {
    "chinese": "玖意",
    "pinyin": "jiǔ yì",
    "meaning": "black jade, intent"
  },
  "Judy Ann": {
    "chinese": "珠蒂安",
    "pinyin": "zhū dì ān",
    "meaning": "pearl stem (flower/leaf) peace"
  },
  "Julia": {
    "chinese": "珠丽雅",
    "pinyin": "zhū lì yǎ",
    "meaning": "beautiful, elegant pearl"
  },
  "Juliet": {
    "chinese": "珠丽叶",
    "pinyin": "zhū lì yè",
    "meaning": "official transliteration: pearl, beauty, leaf"
  },
  "June": {
    "chinese": "珠妮",
    "pinyin": "zhū nī",
    "meaning": "pearl girl"
  },
  "Juniper": {
    "chinese": "珠霓瀑尔",
    "pinyin": "zhū ní pù ěr",
    "meaning": "pearl, rainbow, waterfall, you (classical)"
  },
  "Kade": {
    "chinese": "凯德",
    "pinyin": "kǎi dé",
    "meaning": "triumphant virtue"
  },
  "Kahilla": {
    "chinese": "凯拉",
    "pinyin": "kǎi lā",
    "meaning": "triumphant pull"
  },
  "Kaia": {
    "chinese": "凯雅",
    "pinyin": "kǎi yǎ",
    "meaning": "triumphant elegance"
  },
  "Kaili": {
    "chinese": "凯丽",
    "pinyin": "kǎi lì",
    "meaning": "triumph, beautiful"
  },
  "Kala": {
    "chinese": "卡拉",
    "pinyin": "kǎ lā",
    "meaning": "ka + pull"
  },
  "Kalanie": {
    "chinese": "卡拉霓",
    "pinyin": "kǎ lā ní",
    "meaning": "ka + pull + rainbow"
  },
  "Kalea": {
    "chinese": "卡蕾雅",
    "pinyin": "kǎ lèi yǎ",
    "meaning": "ka, flower bud, graceful"
  },
  "Kalie": {
    "chinese": "卡丽",
    "pinyin": "kǎ lì",
    "meaning": "ka + beautiful"
  },
  "Kalypso": {
    "chinese": "卡丽霹首",
    "pinyin": "kǎ lì pī shǒu",
    "meaning": "ka + beautiful"
  },
  "Kamila": {
    "chinese": "卡蜜拉",
    "pinyin": "kǎ mì lā",
    "meaning": "ka + honey + pull"
  },
  "Kana": {
    "chinese": "卡娜",
    "pinyin": "kǎ nà",
    "meaning": "ka + graceful"
  },
  "Karol": {
    "chinese": "卡柔",
    "pinyin": "kǎ róu",
    "meaning": "ka, gentle"
  },
  "Kasbon": {
    "chinese": "凯愫琫",
    "pinyin": "kǎi sù běng",
    "meaning": "triumphant, sincere, gem ornament of a sword scabbard"
  },
  "Kat": {
    "chinese": "卡特",
    "pinyin": "kǎ tè",
    "meaning": "ka + special"
  },
  "Kate": {
    "chinese": "凯特",
    "pinyin": "kǎi tè",
    "meaning": "triumph + special"
  },
  "Katherine": {
    "chinese": "卡特尔琳",
    "pinyin": "kǎ tè ěr lín",
    "meaning": "ka + unique + you (classical) + lin"
  },
  "Katorea": {
    "chinese": "卡透黎雅",
    "pinyin": "kǎ tòu lí yǎ",
    "meaning": "ka + transparent + Dark (Zayne's Li) + elegance"
  },
  "Kayuna": {
    "chinese": "卡玉娜",
    "pinyin": "kǎ yù nà",
    "meaning": "ka + jade + graceful"
  },
  "Kei": {
    "chinese": "凯",
    "pinyin": "kǎi",
    "meaning": "triumph"
  },
  "Kelli": {
    "chinese": "克丽",
    "pinyin": "kè lì",
    "meaning": "overcome, beauty"
  },
  "Kenzie": {
    "chinese": "恳吉",
    "pinyin": "kěn jí",
    "meaning": "willing, lucky"
  },
  "Khai": {
    "chinese": "凯",
    "pinyin": "kǎi",
    "meaning": "triumph"
  },
  "Khalisa": {
    "chinese": "卡丽洒",
    "pinyin": "kǎ lì sǎ",
    "meaning": "ka + beautiful, carefree"
  },
  "Kiah": {
    "chinese": "琪雅",
    "pinyin": "qí yǎ",
    "meaning": "fine jade elegance"
  },
  "Kiana": {
    "chinese": "琪安娜",
    "pinyin": "qí ān nà",
    "meaning": "fine jade, peace, graceful"
  },
  "Kiki": {
    "chinese": "琪琦，吉吉，可可",
    "pinyin": "qí qí, jí jí, kě kě",
    "meaning": "fine precious jade, lucky luck, can do"
  },
  "Kim": {
    "chinese": "琪睦",
    "pinyin": "qí mù",
    "meaning": "harmonious fine jade"
  },
  "Kimberly": {
    "chinese": "琪霂贝而丽",
    "pinyin": "qí mù bèi ér lì",
    "meaning": "fine jade, treasure and beauty"
  },
  "Kinlay": {
    "chinese": "亲蕾；金蕾",
    "pinyin": "qīn lèi ; jīn lèi",
    "meaning": "intimate flower/leaf bud; gold flower/leaf bud"
  },
  "Kiri": {
    "chinese": "琪丽",
    "pinyin": "qí lì",
    "meaning": "fine jade, beautiful"
  },
  "Kirsten": {
    "chinese": "琪里斯滕",
    "pinyin": "qí lǐ sī téng",
    "meaning": "standard for kirsten, means fine jade inside this vine"
  },
  "Kisara": {
    "chinese": "琪莎拉",
    "pinyin": "qí shā lā",
    "meaning": "fine jade, sedge grass/fern, pull"
  },
  "Kisoo": {
    "chinese": "琪苏 / 秦苏滨",
    "pinyin": "qí sū / qín sū bīn",
    "meaning": "fine jade, revive / Sylus's Qin, revive, along the water"
  },
  "Kite": {
    "chinese": "凯特",
    "pinyin": "kǎi tè",
    "meaning": "triumph, unique"
  },
  "Kiyoko": {
    "chinese": "琪优蔻",
    "pinyin": "qí yōu kòu",
    "meaning": "fine jade, exceptional, cardamom"
  },
  "Klaerea": {
    "chinese": "克蕾丽雅",
    "pinyin": "kè lěi lì yǎ",
    "meaning": "overcome + flower bud + beautiful + elegance"
  },
  "Komal": {
    "chinese": "蔻玛尔",
    "pinyin": "kòu mǎ ěr",
    "meaning": "cardamom, agate, you (classical)"
  },
  "Kriso": {
    "chinese": "克丽锼",
    "pinyin": "kè lì sōu",
    "meaning": "overcome, beauty, engrave"
  },
  "Krista": {
    "chinese": "克丽丝达",
    "pinyin": "kè lì sī dá",
    "meaning": "overcome, beauty, silk, reach"
  },
  "Kristen": {
    "chinese": "克丽丝腾",
    "pinyin": "kè lì sī téng",
    "meaning": "overcome, beautiful, silk, soaring/galloping"
  },
  "Kristina": {
    "chinese": "克丽丝婷",
    "pinyin": "kè lì sī tīng",
    "meaning": "overcome, beautiful, silk, graceful"
  },
  "Krystal": {
    "chinese": "克丽丝朵",
    "pinyin": "kè lì sī duǒ",
    "meaning": "overcome beautiful silk flower"
  },
  "Kuki": {
    "chinese": "喾绮",
    "pinyin": "kù qǐ",
    "meaning": "legendary Emperor, beautiful"
  },
  "Kushi": {
    "chinese": "喾希",
    "pinyin": "kù xī",
    "meaning": "legendary Emperor, happiness"
  },
  "Kylee": {
    "chinese": "凯丽",
    "pinyin": "kǎi lì",
    "meaning": "triumphant beauty"
  },
  "Kyomi": {
    "chinese": "琪优蜜",
    "pinyin": "qí yōu mì",
    "meaning": "fine jade, exceptional honey"
  },
  "Lala": {
    "chinese": "拉拉",
    "pinyin": "lā lā",
    "meaning": "pull pull"
  },
  "Lamia": {
    "chinese": "拉蜜雅",
    "pinyin": "lā mì yǎ",
    "meaning": "pull honey elegance"
  },
  "Lara": {
    "chinese": "拉拉 ; 安怡",
    "pinyin": "lā lá ; ān yí",
    "meaning": "official transliteration: pull pull. translation: peaceful and cheerful"
  },
  "Lass": {
    "chinese": "拉丝",
    "pinyin": "lā sī",
    "meaning": "pull silk"
  },
  "Laura": {
    "chinese": "罗拉, 劳拉",
    "pinyin": "luó lā, láo lā",
    "meaning": "net, pull"
  },
  "Laurett": {
    "chinese": "罗热特",
    "pinyin": "luó rè tè",
    "meaning": "net + hot + special"
  },
  "Laurine": {
    "chinese": "罗琳",
    "pinyin": "luó lín",
    "meaning": "net, gem"
  },
  "Lavender": {
    "chinese": "拉奔达尔",
    "pinyin": "lā bēn dá ěr",
    "meaning": "pull, rush, reach, you (classical)"
  },
  "Lawson": {
    "chinese": "涝森",
    "pinyin": "lào sēn",
    "meaning": "flooded, forest"
  },
  "Layla": {
    "chinese": "来拉 / 蕾拉",
    "pinyin": "lái lā / lěi lā",
    "meaning": "arrival pull / kind pull"
  },
  "Lea": {
    "chinese": "丽雅",
    "pinyin": "lì yǎ",
    "meaning": "beautiful elegance"
  },
  "Leanne": {
    "chinese": "黎安",
    "pinyin": "lí ān",
    "meaning": "dark (Zayne's Li) + peace"
  },
  "Lee": {
    "chinese": "丽",
    "pinyin": "lì",
    "meaning": "beautiful"
  },
  "Legeia": {
    "chinese": "楽给雅",
    "pinyin": "lè gěi yǎ",
    "meaning": "happiness, give, elegance"
  },
  "Leia": {
    "chinese": "蕾雅",
    "pinyin": "lěi yǎ",
    "meaning": "flower bud, elegant"
  },
  "Leila": {
    "chinese": "蕾拉",
    "pinyin": "lèi lā",
    "meaning": "flower/leaf bud + pull"
  },
  "Lemina": {
    "chinese": "楽蜜娜",
    "pinyin": "lè mì nà",
    "meaning": "happy, honey, graceful"
  },
  "Leona": {
    "chinese": "黎藕娜",
    "pinyin": "lí oū nà",
    "meaning": "Dark (Zayne's Li), lotus, graceful"
  },
  "Lexi": {
    "chinese": "楽希",
    "pinyin": "lè xī",
    "meaning": "happiness hope"
  },
  "Lia": {
    "chinese": "丽雅",
    "pinyin": "lì yǎ",
    "meaning": "beautiful elegance"
  },
  "Lianna": {
    "chinese": "丽安娜",
    "pinyin": "lì ān nà",
    "meaning": "beautiful, peace, graceful"
  },
  "Light": {
    "chinese": "来特 /光",
    "pinyin": "lái tè / guāng",
    "meaning": "arrival, special / translation for light"
  },
  "Lilian": {
    "chinese": "丽莉安",
    "pinyin": "lì lì ān",
    "meaning": "beautiful + jasmine + peace"
  },
  "Lilith": {
    "chinese": "丽莉丝",
    "pinyin": "lì lì sī",
    "meaning": "beautiful jasmine silk"
  },
  "Lily": {
    "chinese": "莉莉",
    "pinyin": "lì lì",
    "meaning": "jasmine"
  },
  "Lime": {
    "chinese": "丽美; 来暮",
    "pinyin": "lì měi ; lái mù",
    "meaning": "beautiful, sunset arrives"
  },
  "Liora": {
    "chinese": "丽藕拉",
    "pinyin": "lì ǒu lā",
    "meaning": "beautiful, lotus root, pull"
  },
  "Lisa": {
    "chinese": "丽杂，丽洒",
    "pinyin": "lì zá, lì sǎ",
    "meaning": "beautiful, mixed; beautiful and carefree/unrestrained"
  },
  "Liyla": {
    "chinese": "来拉 / 来",
    "pinyin": "lái lā / lái",
    "meaning": "arrive + pull / arrival"
  },
  "Lizzy": {
    "chinese": "丽极",
    "pinyin": "lì jí",
    "meaning": "exceptionally beautiful"
  },
  "Loey": {
    "chinese": "罗旖 - 小甜甜",
    "pinyin": "luó yǐ - xiǎo tián tián",
    "meaning": "net + charming / Sweetie (literally: small sweet sweet)"
  },
  "Lorel": {
    "chinese": "罗尔 / 娥楽",
    "pinyin": "luó ěr / é lè",
    "meaning": "net, you (classical) / beautiful, happiness"
  },
  "Lorelei": {
    "chinese": "罗尔涞",
    "pinyin": "luó ěr lái",
    "meaning": "net, you (classical), ripple"
  },
  "Lorraine": {
    "chinese": "罗兰",
    "pinyin": "luó lán",
    "meaning": "net orchid"
  },
  "Lorrany": {
    "chinese": "罗燃霓",
    "pinyin": "luó rán ní",
    "meaning": "net, ignite, rainbow"
  },
  "Lottie": {
    "chinese": "拉缇",
    "pinyin": "lā tì",
    "meaning": "pull, red-orange silk"
  },
  "Lou": {
    "chinese": "露",
    "pinyin": "lù",
    "meaning": "dew"
  },
  "Louna": {
    "chinese": "露 / 露娜",
    "pinyin": "lù / lù nà",
    "meaning": "dew / dew, graceful"
  },
  "Louis": {
    "chinese": "渌意思",
    "pinyin": "lù yì sī",
    "meaning": "clear water, meaning"
  },
  "Louise": {
    "chinese": "露意丝",
    "pinyin": "lù yì sī",
    "meaning": "dew + intent + silk"
  },
  "Lovelia": {
    "chinese": "拉布丽雅",
    "pinyin": "lā bù lì yǎ",
    "meaning": "pull, announce, graceful"
  },
  "Luana": {
    "chinese": "罗安娜",
    "pinyin": "luó ān nà",
    "meaning": "net, peace, graceful"
  },
  "Lucero": {
    "chinese": "露璱柔",
    "pinyin": "lù sè róu",
    "meaning": "dew, bright jade, soft"
  },
  "Lucia": {
    "chinese": "露希雅",
    "pinyin": "lù xī yǎ",
    "meaning": "dew, hope, elegance"
  },
  "Luciana": {
    "chinese": "露希安娜",
    "pinyin": "lù xí ān nà",
    "meaning": "dew, hope, peace, graceful"
  },
  "Lucila": {
    "chinese": "璐希雅",
    "pinyin": "lù xī yǎ",
    "meaning": "beautiful jade, hope, elegance"
  },
  "Lucille": {
    "chinese": "露希尔",
    "pinyin": "lù xī ěr",
    "meaning": "dew, hope, you (classical)"
  },
  "Lucillia": {
    "chinese": "露希雅",
    "pinyin": "lù xī yǎ",
    "meaning": "dew, hope, elegance"
  },
  "Lucky": {
    "chinese": "拉琦",
    "pinyin": "lā qí",
    "meaning": "pull fine jade"
  },
  "Lucy": {
    "chinese": "露丝",
    "pinyin": "lù sī",
    "meaning": "dew, silk"
  },
  "Luli": {
    "chinese": "璐丽",
    "pinyin": "lù lì",
    "meaning": "beautiful jade, beautiful"
  },
  "Lumi": {
    "chinese": "璐蜜",
    "pinyin": "lù mì",
    "meaning": "beautiful jade, honey"
  },
  "Luminas": {
    "chinese": "璐敏娜丝",
    "pinyin": "lù mín nà sī",
    "meaning": "beautiful jade, clever, graceful, silk"
  },
  "Luna": {
    "chinese": "露娜",
    "pinyin": "lù nà",
    "meaning": "dew graceful"
  },
  "Luna Maria": {
    "chinese": "露娜 / 玛丽雅",
    "pinyin": "lù nà / mǎ lì yǎ",
    "meaning": "dew + graceful / agate + beautiful + elegant"
  },
  "Lunaria": {
    "chinese": "露娜黎雅",
    "pinyin": "lù nà lí yǎ",
    "meaning": "dew + graceful + dark (Zayne's Li) + elegance"
  },
  "Lune": {
    "chinese": "露恩",
    "pinyin": "lù ēn",
    "meaning": "dew, kindness"
  },
  "Lunètte": {
    "chinese": "露讷特",
    "pinyin": "lù nè tè",
    "meaning": "dew, ne, special"
  },
  "Lux": {
    "chinese": "楽克丝",
    "pinyin": "lè kè sī",
    "meaning": "happiness, overcome, silk"
  },
  "Luz": {
    "chinese": "露滋",
    "pinyin": "lù zī",
    "meaning": "dew + grows"
  },
  "Lyra": {
    "chinese": "丽拉",
    "pinyin": "lì lā",
    "meaning": "beautiful pull"
  },
  "Mackenzie": {
    "chinese": "玛恳吉",
    "pinyin": "mǎ kěn jí",
    "meaning": "agate, willing, lucky"
  },
  "Madeline": {
    "chinese": "玛德琳",
    "pinyin": "mǎ dé lín",
    "meaning": "agate, virtue, gem"
  },
  "Madison": {
    "chinese": "玛蒂森",
    "pinyin": "mǎ dì sēn",
    "meaning": "agate, flower stem, forest"
  },
  "Magnolia": {
    "chinese": "玛格诺丽雅",
    "pinyin": "mǎ gé nuò lì yǎ",
    "meaning": "agate, standard, promise, beautiful, graceful"
  },
  "Malina": {
    "chinese": "玛琳娜",
    "pinyin": "mǎ lín nà",
    "meaning": "agate, gem, graceful"
  },
  "Manda": {
    "chinese": "曼达",
    "pinyin": "màn dá",
    "meaning": "graceful, reaches"
  },
  "Manii": {
    "chinese": "熳妮",
    "pinyin": "màn nī",
    "meaning": "bright-colored/gorgeous girl"
  },
  "Manna": {
    "chinese": "曼娜",
    "pinyin": "màn nà",
    "meaning": "graceful graceful"
  },
  "Mara": {
    "chinese": "玛拉",
    "pinyin": "mǎ lā",
    "meaning": "agate, pull"
  },
  "Marce": {
    "chinese": "玛儿瑟",
    "pinyin": "mǎ ěr sè",
    "meaning": "agate, son, zither"
  },
  "Marcelus": {
    "chinese": "玛儿瑟雷思",
    "pinyin": "mǎ ěr sè léi sī",
    "meaning": "agate, son, zither, thunder, consider"
  },
  "Margaret": {
    "chinese": "玛尔格楽特",
    "pinyin": "mǎ ěr gé lè tè",
    "meaning": "agate + you (classical) + standard + happiness + unique"
  },
  "Mari": {
    "chinese": "玛丽",
    "pinyin": "mǎ lì",
    "meaning": "agate, beautiful"
  },
  "Maria": {
    "chinese": "玛丽雅",
    "pinyin": "mǎ lì yǎ",
    "meaning": "agate, beautiful, elegance"
  },
  "Mariam": {
    "chinese": "玛丽安",
    "pinyin": "mǎ lì ān",
    "meaning": "agate, beautiful, peace"
  },
  "Mariana": {
    "chinese": "玛丽安娜",
    "pinyin": "mǎ lì ān nà",
    "meaning": "agate + beautiful + peace + graceful"
  },
  "Marianne": {
    "chinese": "玛丽安",
    "pinyin": "mǎ lì ān",
    "meaning": "agate + beautiful + peace"
  },
  "Maricia": {
    "chinese": "玛丽喜雅",
    "pinyin": "mǎ lì xí yǎ",
    "meaning": "agate beautiful happy elegance"
  },
  "Mariel": {
    "chinese": "玛丽尔",
    "pinyin": "mǎ lì ěr",
    "meaning": "standard - beautiful agate"
  },
  "Marilee": {
    "chinese": "玛日丽",
    "pinyin": "mǎ rì lì",
    "meaning": "agate, sun, beautiful"
  },
  "Marilyn": {
    "chinese": "美丽琳",
    "pinyin": "měi lì lín",
    "meaning": "beautiful precious gem"
  },
  "Marin": {
    "chinese": "玛琳",
    "pinyin": "mǎ lín",
    "meaning": "agate gem"
  },
  "Marina": {
    "chinese": "玛丽娜",
    "pinyin": "mǎ lì nà",
    "meaning": "gem, beautiful, graceful"
  },
  "Marion": {
    "chinese": "玛丽妍",
    "pinyin": "mǎ lì yán",
    "meaning": "agate, beautiful, beautiful"
  },
  "Marlena": {
    "chinese": "玛尔蕾娜",
    "pinyin": "mǎ ěr lěi nà",
    "meaning": "agate, you (classical), flower bud, graceful"
  },
  "Marlene": {
    "chinese": "玛尔琳",
    "pinyin": "mǎ ěr lín",
    "meaning": "agate, you (classical), gem"
  },
  "Marnie": {
    "chinese": "玛尔妮",
    "pinyin": "mǎ ěr nī",
    "meaning": "agate girl"
  },
  "Mars": {
    "chinese": "马尔斯",
    "pinyin": "mǎ ér sī",
    "meaning": "official transliteration"
  },
  "Maru": {
    "chinese": "玛缛",
    "pinyin": "mǎ rù",
    "meaning": "agate, beautiful"
  },
  "Mary": {
    "chinese": "玛丽",
    "pinyin": "mǎ lì",
    "meaning": "beautiful agate"
  },
  "Mary Anne": {
    "chinese": "玛丽安 / 美安",
    "pinyin": "mǎ lì ān / měi ān",
    "meaning": "agate, beautiful, peaceful / beautiful peace"
  },
  "Maryam": {
    "chinese": "玛丽安",
    "pinyin": "mǎ lì ān",
    "meaning": "agate, beautiful, peace"
  },
  "Maven": {
    "chinese": "玛雯",
    "pinyin": "mǎ wén",
    "meaning": "agate + colorful clouds"
  },
  "Mavis": {
    "chinese": "玛碧丝",
    "pinyin": "mǎ bì sī",
    "meaning": "agate, jade, silk"
  },
  "Maya": {
    "chinese": "霾雅",
    "pinyin": "mái yǎ",
    "meaning": "elegant haze"
  },
  "Mayu Xia": {
    "chinese": "夏玛玉，夏霾玉",
    "pinyin": "xià mǎ yù, xià mái yù",
    "meaning": "summer, agate, jade; summer, haze, jade"
  },
  "Meera": {
    "chinese": "蜜拉",
    "pinyin": "mì lā",
    "meaning": "pull honey"
  },
  "Megan": {
    "chinese": "美感",
    "pinyin": "měi gǎn",
    "meaning": "beautiful feeling"
  },
  "Mei": {
    "chinese": "美",
    "pinyin": "měi",
    "meaning": "beauty"
  },
  "Mei Mei": {
    "chinese": "美美",
    "pinyin": "měi měi",
    "meaning": "beautiful beautiful"
  },
  "Meini": {
    "chinese": "美妮",
    "pinyin": "měi nī",
    "meaning": "beautiful girl"
  },
  "Melanie": {
    "chinese": "美拉妮",
    "pinyin": "měi lā nī",
    "meaning": "beautiful pull girl"
  },
  "Melati": {
    "chinese": "美拉缇",
    "pinyin": "měi lā tì",
    "meaning": "beautiful, pull, red-orange silk"
  },
  "Melissa": {
    "chinese": "美丽洒",
    "pinyin": "měi lì sǎ",
    "meaning": "beautiful and carefree"
  },
  "Meljane": {
    "chinese": "美楽嘉恩",
    "pinyin": "měi lè jiā ēn",
    "meaning": "beautiful, happy, auspicious, kindness"
  },
  "Melody": {
    "chinese": "美楽蒂",
    "pinyin": "měi lè dì",
    "meaning": "beautiful, happy, flower stem"
  },
  "Melova": {
    "chinese": "美楼芭",
    "pinyin": "měi lóu bā",
    "meaning": "beautiful, tower, fragrant plant"
  },
  "Mena": {
    "chinese": "美娜",
    "pinyin": "měi nà",
    "meaning": "beautiful gracefulness"
  },
  "Menna": {
    "chinese": "璊娜",
    "pinyin": "mén nà",
    "meaning": "red jade, graceful"
  },
  "Mercy": {
    "chinese": "么尔希",
    "pinyin": "me ěr xī",
    "meaning": "me + you (classical) + happiness"
  },
  "Merliah": {
    "chinese": "美尔丽雅",
    "pinyin": "měi ěr lì yǎ",
    "meaning": "beautiful, you (classical), beautiful, elegant"
  },
  "Meta": {
    "chinese": "美塔",
    "pinyin": "měi tǎ",
    "meaning": "beautiful pagoda"
  },
  "Mia": {
    "chinese": "蜜雅",
    "pinyin": "mì yǎ",
    "meaning": "honey elegance"
  },
  "Mica": {
    "chinese": "蜜卡",
    "pinyin": "mì kǎ",
    "meaning": "honey, ka"
  },
  "Michelle": {
    "chinese": "米歇尔，蜜勰尔",
    "pinyin": "mǐ xiē ěr, mì xié ěr",
    "meaning": "official translit: rice, rest, you (classical); ours: honey, harmonious, you (classical)"
  },
  "Mielko": {
    "chinese": "蜜叶口",
    "pinyin": "mì yè kǒu",
    "meaning": "honey leaf + ko"
  },
  "Mik": {
    "chinese": "蜜可",
    "pinyin": "mì kě",
    "meaning": "honey, can"
  },
  "Mika": {
    "chinese": "蜜卡",
    "pinyin": "mì kǎ",
    "meaning": "honey + ka (literally Card)"
  },
  "Mikaela": {
    "chinese": "蜜凯拉",
    "pinyin": "mì kǎi lā",
    "meaning": "honey, triumphant, pull"
  },
  "Mikaila": {
    "chinese": "蜜凯拉",
    "pinyin": "mì kǎi là",
    "meaning": "honey triumph pulls"
  },
  "Mikei": {
    "chinese": "蜜凯",
    "pinyin": "mì kǎi",
    "meaning": "honey triumph"
  },
  "Mila": {
    "chinese": "蜜拉",
    "pinyin": "mì lā",
    "meaning": "honey pull"
  },
  "Milene": {
    "chinese": "蜜楽恩",
    "pinyin": "mì lè ēn",
    "meaning": "honey, happiness, kindness"
  },
  "Milky": {
    "chinese": "蜜乳喜/琪",
    "pinyin": "mì rǔ xǐ/qí",
    "meaning": "honey milk enjoy/jade"
  },
  "Milli": {
    "chinese": "蜜丽",
    "pinyin": "mì lì",
    "meaning": "honey, beautiful"
  },
  "Milo": {
    "chinese": "霾蒌",
    "pinyin": "mái lóu",
    "meaning": "haze, mugwort"
  },
  "Mimi": {
    "chinese": "蜜蜜",
    "pinyin": "mì mì",
    "meaning": "honey honey"
  },
  "Mina": {
    "chinese": "敏娜",
    "pinyin": "mǐn nà",
    "meaning": "intelligent, graceful"
  },
  "Minnie": {
    "chinese": "蜜妮",
    "pinyin": "mì nī",
    "meaning": "honey girl"
  },
  "Minty": {
    "chinese": "敏琪 or 薄荷",
    "pinyin": "mǐn qí or bò hé",
    "meaning": "clever/intelligent fine jade or mint"
  },
  "Mira": {
    "chinese": "蜜拉",
    "pinyin": "mì lā",
    "meaning": "honey pull"
  },
  "Mirella": {
    "chinese": "美尔拉",
    "pinyin": "měi ěr lā",
    "meaning": "beautiful, you (classical), pull"
  },
  "Misha": {
    "chinese": "蜜霞",
    "pinyin": "mì xiá",
    "meaning": "honey sunset/rosy sky"
  },
  "Missy": {
    "chinese": "蜜希 / 蜜丝",
    "pinyin": "mì xī / mì sī",
    "meaning": "honey, hope / honey silk"
  },
  "Mitsuki": {
    "chinese": "蜜初琪",
    "pinyin": "mì chū qí",
    "meaning": "honey, beginning, fine jade"
  },
  "Miwa": {
    "chinese": "蜜娃",
    "pinyin": "mì wá",
    "meaning": "honey, doll"
  },
  "Miya": {
    "chinese": "蜜雅",
    "pinyin": "mì yǎ",
    "meaning": "Honey, elegance"
  },
  "Miyu": {
    "chinese": "蜜玉",
    "pinyin": "mì yù",
    "meaning": "honey, jade"
  },
  "Mizu": {
    "chinese": "蜜足",
    "pinyin": "mì zú",
    "meaning": "honey, sufficient"
  },
  "Moge": {
    "chinese": "沫歌",
    "pinyin": "mò gē",
    "meaning": "bubble song"
  },
  "Moka": {
    "chinese": "暮卡",
    "pinyin": "mù kǎ",
    "meaning": "sunset + ka"
  },
  "Moliza": {
    "chinese": "默丽杂",
    "pinyin": "mò lì zá",
    "meaning": "silent, beautiful, mixed"
  },
  "Momo": {
    "chinese": "沫沫",
    "pinyin": "mò mò",
    "meaning": "bubbles"
  },
  "Monica": {
    "chinese": "玛霓卡",
    "pinyin": "mǎ ní kǎ",
    "meaning": "agate + rainbow + ka"
  },
  "Moon": {
    "chinese": "暮恩，月亮",
    "pinyin": "mù ēn, yuè liàng",
    "meaning": "sunset kindness, translation of moon"
  },
  "Morgana": {
    "chinese": "沫尔尕娜",
    "pinyin": "mò ěr gǎ nà",
    "meaning": "bubble, you (classical), little, graceful"
  },
  "Mumtaz": {
    "chinese": "暮塔滋 / 暮暮塔滋",
    "pinyin": "mù tǎ zī / mù mù tǎ zī",
    "meaning": "sunset, pagoda, grow / sunset, sunset, pagoda, grow"
  },
  "Myo": {
    "chinese": "谬 / 妙",
    "pinyin": "miù / miào",
    "meaning": "The first meaning is not good, but it's a direct phonetic match. (absurd); the second is not a perfect match but it means marvelous or clever"
  },
  "Myr": {
    "chinese": "美尔",
    "pinyin": "měi ěr",
    "meaning": "beautiful + you (classical)"
  },
  "Myra": {
    "chinese": "蜜拉",
    "pinyin": "mì lā",
    "meaning": "honey pull"
  },
  "Myriam": {
    "chinese": "蜜丽安",
    "pinyin": "mì lì ān",
    "meaning": "honey, beautiful, peace"
  },
  "Myrtille": {
    "chinese": "美尔特",
    "pinyin": "měi ěr tè",
    "meaning": "beautiful + you (classical) + special"
  },
  "Nadia": {
    "chinese": "娜蒂雅",
    "pinyin": "nà dì yǎ",
    "meaning": "graceful, flower stem, elegance"
  },
  "Nadila": {
    "chinese": "娜蒂拉",
    "pinyin": "nà dì lā",
    "meaning": "graceful, flower stem, pull"
  },
  "Naia": {
    "chinese": "柰雅",
    "pinyin": "nài yǎ",
    "meaning": "elegant crabapple"
  },
  "Naiory": {
    "chinese": "娜优莉",
    "pinyin": "nà yōu lì",
    "meaning": "graceful, exceptional jasmine"
  },
  "Naira": {
    "chinese": "柰拉",
    "pinyin": "nài lā",
    "meaning": "crabapple, pull"
  },
  "Nami": {
    "chinese": "娜蜜",
    "pinyin": "nà mì",
    "meaning": "graceful honey"
  },
  "Namura": {
    "chinese": "娜暮拉",
    "pinyin": "nà mù lā",
    "meaning": "graceful, sunset, pull"
  },
  "Nana": {
    "chinese": "娜娜",
    "pinyin": "nà nà",
    "meaning": "graceful grace"
  },
  "Nanabi": {
    "chinese": "娜娜碧",
    "pinyin": "nà nà bì",
    "meaning": "graceful, graceful, jade"
  },
  "Nanda": {
    "chinese": "南达",
    "pinyin": "nán dá",
    "meaning": "reaches the south"
  },
  "Naomi": {
    "chinese": "娜藕蜜",
    "pinyin": "nà ǒu mì",
    "meaning": "graceful, lotus, honey"
  },
  "Nara": {
    "chinese": "娜拉",
    "pinyin": "nà lā",
    "meaning": "graceful, pull"
  },
  "Nata": {
    "chinese": "娜塔",
    "pinyin": "nà tǎ",
    "meaning": "graceful pagoda"
  },
  "Natalia": {
    "chinese": "娜达丽雅",
    "pinyin": "nà dá lì yǎ",
    "meaning": "graceful, reach, beautiful, elegance"
  },
  "Natalie": {
    "chinese": "娜达丽",
    "pinyin": "nà dá lì",
    "meaning": "graceful, reaches, beauty"
  },
  "Natasha": {
    "chinese": "娜她霞",
    "pinyin": "nà tā xiá",
    "meaning": "graceful, her, sunset/rose-tinted sky"
  },
  "Nathália": {
    "chinese": "娜达丽雅",
    "pinyin": "nà dá lì yǎ",
    "meaning": "graceful, reach, beauty, elegance"
  },
  "Naty": {
    "chinese": "娜蒂",
    "pinyin": "nà dì",
    "meaning": "graceful flower stem"
  },
  "Navillera": {
    "chinese": "娜碧来拉 / 娜碧丽雅",
    "pinyin": "nà bì lái lā / nà bì lì yǎ",
    "meaning": "graceful, jade, arrival, pull / graceful, jade, beautiful, elegance"
  },
  "Naya": {
    "chinese": "柰雅",
    "pinyin": "nài yǎ",
    "meaning": "crabapple, elegance"
  },
  "Nazli": {
    "chinese": "娜紫楽",
    "pinyin": "nà zǐ lè",
    "meaning": "graceful + purple + happiness"
  },
  "Nesa": {
    "chinese": "妮洒",
    "pinyin": "nī sǎ",
    "meaning": "unrestrained/carefree girl"
  },
  "Nezia": {
    "chinese": "内吉雅",
    "pinyin": "nèi jí yǎ",
    "meaning": "inner, luck, elegance"
  },
  "Nezu": {
    "chinese": "内珠",
    "pinyin": "nèi zhū",
    "meaning": "inner pearl"
  },
  "Nia": {
    "chinese": "妮雅",
    "pinyin": "nī yǎ",
    "meaning": "elegant girl"
  },
  "Nicola": {
    "chinese": "霓蔻拉",
    "pinyin": "ní kòu lā",
    "meaning": "rainbow, treasure, pull"
  },
  "Nicole": {
    "chinese": "霓寇尔",
    "pinyin": "ní kòu ěr",
    "meaning": "rainbow, cardamom, you (classical)"
  },
  "Nika": {
    "chinese": "霓卡",
    "pinyin": "ní kǎ",
    "meaning": "rainbow, ka (card)"
  },
  "Nike": {
    "chinese": "妮凯",
    "pinyin": "nī kǎi",
    "meaning": "triumphant girl"
  },
  "Niki": {
    "chinese": "妮琦",
    "pinyin": "nī qí",
    "meaning": "girl + precious jade"
  },
  "Nikki": {
    "chinese": "妮凯",
    "pinyin": "nī kǎi",
    "meaning": "triumphant girl"
  },
  "Nina": {
    "chinese": "霓娜",
    "pinyin": "ní nà",
    "meaning": "rainbow, graceful"
  },
  "Nindha": {
    "chinese": "宁达",
    "pinyin": "níng dá",
    "meaning": "reach peace"
  },
  "Nisa": {
    "chinese": "霓洒",
    "pinyin": "ní sǎ",
    "meaning": "rainbow, carefree"
  },
  "Nitu": {
    "chinese": "霓图",
    "pinyin": "ní tú",
    "meaning": "rainbow drawing"
  },
  "Nixie": {
    "chinese": "妮克希",
    "pinyin": "nī kè xī",
    "meaning": "girl, overcome, hope"
  },
  "Noa": {
    "chinese": "诺雅",
    "pinyin": "nuó yǎ",
    "meaning": "elegant promise"
  },
  "Noelle": {
    "chinese": "诺叶楽",
    "pinyin": "nuò yè lè",
    "meaning": "promise, leaf, joy"
  },
  "Nollaig": {
    "chinese": "娜楽格",
    "pinyin": "nà lè gé",
    "meaning": "graceful, happiness, standard"
  },
  "Noshi": {
    "chinese": "娜希",
    "pinyin": "nà xī",
    "meaning": "graceful hope"
  },
  "Nym": {
    "chinese": "宁",
    "pinyin": "níng",
    "meaning": "tranquil"
  },
  "Nymphelia": {
    "chinese": "宁菲丽雅",
    "pinyin": "níng fēi lì yǎ",
    "meaning": "tranquil, fragrant, beautiful, elegant"
  },
  "Nyx": {
    "chinese": "霓克璱",
    "pinyin": "ní kè sè",
    "meaning": "rainbow, overcome, bright jade"
  },
  "Nyza": {
    "chinese": "妮杂",
    "pinyin": "nī zá",
    "meaning": "girl mixed"
  },
  "Ocha": {
    "chinese": "藕卡 / 藕茶",
    "pinyin": "ǒu kǎ / ǒu chá",
    "meaning": "lotus + ka / lotus + tea"
  },
  "Olha": {
    "chinese": "藕楽雅",
    "pinyin": "ǒu lè yǎ",
    "meaning": "happy elegant lotus"
  },
  "Olivia": {
    "chinese": "藕丽碧雅",
    "pinyin": "ǒu lì bì yǎ",
    "meaning": "lotus, beautiful, jade, elegance"
  },
  "Paige": {
    "chinese": "佩吉",
    "pinyin": "pèi jí",
    "meaning": "jade pendant + lucky"
  },
  "Pam": {
    "chinese": "琶暮",
    "pinyin": "pá mù",
    "meaning": "pipa, sunset"
  },
  "Patricia": {
    "chinese": "琶缇丽希雅",
    "pinyin": "pá tí lì xī yǎ",
    "meaning": "pipa, red/orange silk, beautiful, hope, elegance"
  },
  "Patti": {
    "chinese": "琶缇",
    "pinyin": "pá tí",
    "meaning": "pipa, red/orange silk"
  },
  "Paula": {
    "chinese": "泡拉",
    "pinyin": "pào lā",
    "meaning": "bubble, pull"
  },
  "Payel": {
    "chinese": "琶夜如",
    "pinyin": "pā yè rú",
    "meaning": "like pipa night"
  },
  "Peachy": {
    "chinese": "碧琪",
    "pinyin": "bì qí",
    "meaning": "fine jade"
  },
  "Pearl": {
    "chinese": "佩尔楽",
    "pinyin": "pèi ěr lè",
    "meaning": "jade pendant, (classical), happiness"
  },
  "Penelope": {
    "chinese": "佩讷罗霹",
    "pinyin": "pèi nè luó pī",
    "meaning": "jade pendant + ne + net + thunderclap"
  },
  "Penumbra": {
    "chinese": "佩娜暮捗拉",
    "pinyin": "pèi nà mù bù lā",
    "meaning": "jade pendant, graceful, sunset, make progress, pull"
  },
  "Perla": {
    "chinese": "瀑尔拉",
    "pinyin": "pù ěr lā",
    "meaning": "waterfall, you (classical), pull"
  },
  "Persephone": {
    "chinese": "珀尔塞芙妮",
    "pinyin": "pò ěr sāi fú nī",
    "meaning": "standard transliteration"
  },
  "Pia": {
    "chinese": "碧雅",
    "pinyin": "bì yǎ",
    "meaning": "jade elegance"
  },
  "Pija": {
    "chinese": "霹嘉",
    "pinyin": "pī jiā",
    "meaning": "thunderclap, auspicious"
  },
  "Pitta": {
    "chinese": "霹塔",
    "pinyin": "pī tǎ",
    "meaning": "thunderclap pagoda"
  },
  "Playboi Carti": {
    "chinese": "卡尔提玩咖",
    "pinyin": "kǎ ěr tí wān kā",
    "meaning": "ka + you (classical) + raise + translation of Playboy"
  },
  "Poala": {
    "chinese": "珀阿拉",
    "pinyin": "pò ā lā",
    "meaning": "amber pull"
  },
  "Priscella Jane": {
    "chinese": "佩丽拉，杰恩",
    "pinyin": "pèi lì lā, jié ēn",
    "meaning": "jade pendant, beautiful, pull, heroic, kindness"
  },
  "Pulmo": {
    "chinese": "瀑楽沫",
    "pinyin": "pù lè mò",
    "meaning": "pond, happiness, bubbles"
  },
  "Quin": {
    "chinese": "可维音",
    "pinyin": "kě wéi yīn",
    "meaning": "approve maintain sound"
  },
  "Rachel": {
    "chinese": "蕾彻尔",
    "pinyin": "lěi chè ěr",
    "meaning": "flower bud, thorough (Sylus's che), you (classical)"
  },
  "Rae": {
    "chinese": "瑞",
    "pinyin": "ruì",
    "meaning": "auspicious"
  },
  "Raine": {
    "chinese": "类恩",
    "pinyin": "lèi ēn",
    "meaning": "type, kindness"
  },
  "Ran": {
    "chinese": "珃",
    "pinyin": "rán",
    "meaning": "jade"
  },
  "Rani": {
    "chinese": "珃霓",
    "pinyin": "rǎn ní",
    "meaning": "jade rainbow"
  },
  "Rania": {
    "chinese": "拉霓雅",
    "pinyin": "lā ní yǎ",
    "meaning": "pull + rainbow + elegance"
  },
  "Raphaela": {
    "chinese": "拉菲尔拉",
    "pinyin": "lā fēi ěr lā",
    "meaning": "pull, fragrant, you (classical), pull"
  },
  "Rari": {
    "chinese": "拉丽",
    "pinyin": "lā lì",
    "meaning": "pull beauty"
  },
  "Raywin": {
    "chinese": "来雯 / 雷雯",
    "pinyin": "lái wén / léi wén",
    "meaning": "colorful clouds arrive / flower buds, colorful clouds"
  },
  "Razielle": {
    "chinese": "拉紫尔",
    "pinyin": "lā zǐ ěr",
    "meaning": "pull, purple, you (classical)"
  },
  "Rea": {
    "chinese": "丽雅",
    "pinyin": "lì yǎ",
    "meaning": "beautiful elegance"
  },
  "Redhia": {
    "chinese": "楽蒂雅",
    "pinyin": "lè dì yǎ",
    "meaning": "joy, standard, graceful"
  },
  "Reen": {
    "chinese": "琳",
    "pinyin": "lín",
    "meaning": "gem"
  },
  "Rei": {
    "chinese": "蕾",
    "pinyin": "lèi",
    "meaning": "flower/leaf bud"
  },
  "Reina": {
    "chinese": "蕾娜",
    "pinyin": "lěi nà",
    "meaning": "graceful buds (trees/flowers)"
  },
  "Reisa": {
    "chinese": "蕾洒",
    "pinyin": "lěi sǎ",
    "meaning": "flower bud, carefree"
  },
  "Reishlyn": {
    "chinese": "蕾希琳",
    "pinyin": "lěi xī lín",
    "meaning": "flower bud, hope, forest"
  },
  "Relle": {
    "chinese": "瑞丽",
    "pinyin": "ruì lì",
    "meaning": "auspicious beauty"
  },
  "Remi": {
    "chinese": "蕾蜜",
    "pinyin": "lěi mì",
    "meaning": "flower bud, honey"
  },
  "Ren": {
    "chinese": "仁",
    "pinyin": "rén",
    "meaning": "kindness"
  },
  "Renée": {
    "chinese": "蕾内",
    "pinyin": "lěi nèi",
    "meaning": "flower bud, inner"
  },
  "Reverie": {
    "chinese": "瑞芙丽",
    "pinyin": "ruì fú lì",
    "meaning": "auspicious, lotus, beauty"
  },
  "Rhea": {
    "chinese": "丽雅",
    "pinyin": "lì yǎ",
    "meaning": "beautiful, elegance"
  },
  "Rheanne": {
    "chinese": "黎安",
    "pinyin": "lí ān",
    "meaning": "Dark (Zayne's Li) peace"
  },
  "Rhiane": {
    "chinese": "丽安",
    "pinyin": "lì ān",
    "meaning": "beautiful, graceful"
  },
  "Rhoza": {
    "chinese": "柔杂",
    "pinyin": "róu zá",
    "meaning": "soft + mixed"
  },
  "Rian Miri": {
    "chinese": "丽安蜜丽",
    "pinyin": "lì ān mì lì",
    "meaning": "beautiful peace, honey beauty"
  },
  "Rianna": {
    "chinese": "莉安娜 or 丽安娜",
    "pinyin": "lì ānnà",
    "meaning": "jasmine peace elegance or beautiful peace elegance"
  },
  "Rila": {
    "chinese": "丽拉",
    "pinyin": "lì lā",
    "meaning": "beautiful pull"
  },
  "Ritcher": {
    "chinese": "黎琦尔",
    "pinyin": "lí qí ěr",
    "meaning": "Dark (Zayne's Li), precious jade, you"
  },
  "Riva": {
    "chinese": "丽芭",
    "pinyin": "lì bā",
    "meaning": "beautiful fragrant plant"
  },
  "Rivaille": {
    "chinese": "丽芭尔",
    "pinyin": "lì bā ěr",
    "meaning": "beautiful, fragrant plant, you (classical)"
  },
  "Rizka": {
    "chinese": "黎希卡",
    "pinyin": "lí xī kǎ",
    "meaning": "Dark (Zayne's Li), hope, ka"
  },
  "Robersy": {
    "chinese": "拉布尔喜",
    "pinyin": "lā bù ěr xǐ",
    "meaning": "pull + announce + you (classical) + happiness"
  },
  "Ronnie": {
    "chinese": "燃霓",
    "pinyin": "rán ní",
    "meaning": "ignite rainbow"
  },
  "Rosa": {
    "chinese": "柔萨",
    "pinyin": "róu sà",
    "meaning": "soft bodhisattva"
  },
  "Rosalyn": {
    "chinese": "柔洒丽雅",
    "pinyin": "róu sǎ lì yǎ",
    "meaning": "soft, unrestrained/carefree, beautiful, elegance"
  },
  "Rosario": {
    "chinese": "柔洒丽藕",
    "pinyin": "róu sǎ lì ǒu",
    "meaning": "soft, unrestrained/carefree, beautiful lotus"
  },
  "Rosarya": {
    "chinese": "罗萨丽雅",
    "pinyin": "luó sà lì yǎ",
    "meaning": "net, boddhitsatva, beautiful, elegant"
  },
  "Rose": {
    "chinese": "柔丝",
    "pinyin": "róu sī",
    "meaning": "soft silk"
  },
  "Roslan": {
    "chinese": "柔丝兰",
    "pinyin": "róu sī lán",
    "meaning": "soft silk orchid"
  },
  "Rosy": {
    "chinese": "柔希",
    "pinyin": "róu xī",
    "meaning": "soft hope"
  },
  "Rou": {
    "chinese": "柔",
    "pinyin": "róu",
    "meaning": "soft and gentle"
  },
  "Rua": {
    "chinese": "缛阿",
    "pinyin": "rù ā",
    "meaning": "beautiful + a"
  },
  "Ruby": {
    "chinese": "缛碧",
    "pinyin": "rù bì",
    "meaning": "beautiful jade"
  },
  "Ruhan": {
    "chinese": "缛寒",
    "pinyin": "rù hán",
    "meaning": "beautiful winter/cold"
  },
  "Runa": {
    "chinese": "缛娜",
    "pinyin": "rù nà",
    "meaning": "beautiful, graceful"
  },
  "Rya": {
    "chinese": "丽雅",
    "pinyin": "lì yǎ",
    "meaning": "beautiful elegance"
  },
  "Ryn": {
    "chinese": "琳",
    "pinyin": "lín",
    "meaning": "gem"
  },
  "Saba": {
    "chinese": "璱芭 / 萨芭",
    "pinyin": "sè bā / sà bā",
    "meaning": "bright jade, fragrant plant / bodhisattva, fragrant plant"
  },
  "Sabrina": {
    "chinese": "洒布琳娜",
    "pinyin": "sǎ bù lín nà",
    "meaning": "carefree/unrestrained, announce, gem, graceful"
  },
  "Sachi": {
    "chinese": "萨起",
    "pinyin": "sà qǐ",
    "meaning": "bodhisattva, rise"
  },
  "Saeka": {
    "chinese": "赛娥卡",
    "pinyin": "sài é kǎ",
    "meaning": "competition, pretty woman, ka"
  },
  "Sage": {
    "chinese": "谁杰",
    "pinyin": "shuí jié",
    "meaning": "who, heroic"
  },
  "Sakura": {
    "chinese": "萨喾拉",
    "pinyin": "sà kù lā",
    "meaning": "bodhisattva legendary Emperor pulls (there is no nice meaning ku in Chinese)"
  },
  "Salma": {
    "chinese": "萨楽玛",
    "pinyin": "sà lè mǎ",
    "meaning": "bodhisattva, happy agate"
  },
  "Salsa": {
    "chinese": "洒露萨",
    "pinyin": "sǎ lù sà",
    "meaning": "carefree/unrestrained dew bodhisattva"
  },
  "Sam": {
    "chinese": "洒暮",
    "pinyin": "sǎ mù",
    "meaning": "carefree sunset"
  },
  "Samantha": {
    "chinese": "萨曼莎",
    "pinyin": "sà màn shā",
    "meaning": "official transliteration: bodhisattva, graceful, sedge grass/fern"
  },
  "Samira": {
    "chinese": "洒蜜拉",
    "pinyin": "sǎ mì lā",
    "meaning": "carefree/unrestrained, honey, pulls"
  },
  "Sammy": {
    "chinese": "萨蜜",
    "pinyin": "sà mì",
    "meaning": "bodhisattva, honey"
  },
  "Sana": {
    "chinese": "珊娜，萨娜",
    "pinyin": "shān nà, sà nà",
    "meaning": "graceful coral, graceful bodhittsatva"
  },
  "Sanne": {
    "chinese": "洒娜",
    "pinyin": "sǎ nà",
    "meaning": "carefree/unrestrained + graceful"
  },
  "Sanya": {
    "chinese": "三雅 / 善雅",
    "pinyin": "sān yǎ / shàn yǎ",
    "meaning": "three, elegance (phonetic match), kind elegance"
  },
  "Sara": {
    "chinese": "萨拉",
    "pinyin": "sà lā",
    "meaning": "bodhisattva, pull"
  },
  "Sarah": {
    "chinese": "萨拉",
    "pinyin": "sà lā",
    "meaning": "bodhisattva pulls"
  },
  "Sasha": {
    "chinese": "萨霞",
    "pinyin": "sà xiá",
    "meaning": "bodhisattva, sunset/rosy sky"
  },
  "Sayali": {
    "chinese": "赛黎",
    "pinyin": "sài lí",
    "meaning": "compete, Dark (Zayne's Li)"
  },
  "Sayuri": {
    "chinese": "萨玉丽",
    "pinyin": "sà yù lì",
    "meaning": "bodhattsitva jade beauty"
  },
  "Scarlet": {
    "chinese": "苏卡蕾特",
    "pinyin": "sū kǎ lěi tè",
    "meaning": "revive + ka (card) + flower/leaf bud, unique"
  },
  "Sea": {
    "chinese": "溪 ; 小海",
    "pinyin": "xī ; xiǎo hǎi",
    "meaning": "transliteration: stream, translation: little ocean"
  },
  "Seiko": {
    "chinese": "赛蔻，丝爱蔻",
    "pinyin": "sài kòu, sī ài kòu",
    "meaning": "compete, treasure, ka, silk, love, ka"
  },
  "Seira": {
    "chinese": "赛拉",
    "pinyin": "sài lā",
    "meaning": "competitive pull"
  },
  "Selena": {
    "chinese": "璱琳娜",
    "pinyin": "sè lín nà",
    "meaning": "bright jade, gem, elegance"
  },
  "Selene": {
    "chinese": "璱琳",
    "pinyin": "sè lín",
    "meaning": "bright jade gem"
  },
  "Senna": {
    "chinese": "森娜",
    "pinyin": "sēn nà",
    "meaning": "graceful forest"
  },
  "Sephora": {
    "chinese": "璱紑拉",
    "pinyin": "sè fū lā",
    "meaning": "bright jade, bright silk, pull"
  },
  "Septia": {
    "chinese": "璱琣蒂雅",
    "pinyin": "sè běng dì yǎ",
    "meaning": "bright jade, jade pendant, flower stem, elegance"
  },
  "Sera": {
    "chinese": "璱拉",
    "pinyin": "sè lā",
    "meaning": "bright jade, pull"
  },
  "Seraphina": {
    "chinese": "璱拉菲娜",
    "pinyin": "sè lā fēi nà",
    "meaning": "bright jade, pull, fragrant, graceful"
  },
  "Seraphine": {
    "chinese": "璱拉菲恩",
    "pinyin": "sè lā fēi ēn",
    "meaning": "bright jade, pull, fragrant plant, kindness"
  },
  "Serena Li": {
    "chinese": "黎 璱琳娜",
    "pinyin": "lí sè lín nà",
    "meaning": "Dark/Li (Like Zayne's Li), bright jade, sound of gems, elegance"
  },
  "Shaaa": {
    "chinese": "莎，霞",
    "pinyin": "shā, xiá",
    "meaning": "sedge grass, sunset/rosy sky"
  },
  "Shai": {
    "chinese": "晒",
    "pinyin": "shài",
    "meaning": "bask in the sun"
  },
  "Sharika": {
    "chinese": "霞丽卡",
    "pinyin": "xiá lì kǎ",
    "meaning": "sunset/rosy sky, beautiful, ka"
  },
  "Sharon": {
    "chinese": "沙燃",
    "pinyin": "shā rǎn",
    "meaning": "sedge grass/fern + ignite"
  },
  "Shay": {
    "chinese": "谁 / 谁雅 / 晒雅",
    "pinyin": "shuí / shuí yǎ / shài yǎ",
    "meaning": "who / who, elegance / bask in sun, elegance"
  },
  "Sheelou": {
    "chinese": "希露",
    "pinyin": "xī lù",
    "meaning": "hope, dew"
  },
  "Sheen": {
    "chinese": "溪恩",
    "pinyin": "xī ēn",
    "meaning": "kind stream"
  },
  "Sheinn": {
    "chinese": "晒恩",
    "pinyin": "shài ēn",
    "meaning": "bask in sunlight, kindness"
  },
  "Shella": {
    "chinese": "射拉 ; 谢拉",
    "pinyin": "shè lā / xiè lā",
    "meaning": "shoot + pull (best pronunciation) ; thanks + pull"
  },
  "Shelly": {
    "chinese": "希丽",
    "pinyin": "xī lì",
    "meaning": "beautiful hope"
  },
  "Shelsey": {
    "chinese": "射尔希",
    "pinyin": "shè ěr xī",
    "meaning": "shoot, (classical), hope"
  },
  "Shera": {
    "chinese": "璱拉",
    "pinyin": "sè lā",
    "meaning": "bright jade pull"
  },
  "Sia": {
    "chinese": "丝雅",
    "pinyin": "sī yǎ",
    "meaning": "silk elegance"
  },
  "Sienna": {
    "chinese": "希恩娜",
    "pinyin": "xī ēn nà",
    "meaning": "hope, kindness, graceful"
  },
  "Sire": {
    "chinese": "希尔",
    "pinyin": "xī ěr",
    "meaning": "hope you"
  },
  "Sisilim": {
    "chinese": "丝丝琳",
    "pinyin": "sī sī lín",
    "meaning": "silky silk gem"
  },
  "Siu": {
    "chinese": "希玉，希佑",
    "pinyin": "xī yù, xī yòu",
    "meaning": "hope, jade; hope, blessing"
  },
  "Skye": {
    "chinese": "丝凯",
    "pinyin": "sī kǎi",
    "meaning": "silk, triumphant"
  },
  "Skylar": {
    "chinese": "丝凯拉",
    "pinyin": "sī kǎi lā",
    "meaning": "silk, triumph, pull"
  },
  "Sofia": {
    "chinese": "锼菲雅",
    "pinyin": "sōu fēi yǎ",
    "meaning": "engrave, fragrant, elegance"
  },
  "Sofiia": {
    "chinese": "锼菲雅",
    "pinyin": "sōu fēi yǎ",
    "meaning": "engrave, fragrant elegance"
  },
  "Sol": {
    "chinese": "锼楽",
    "pinyin": "sōu lè",
    "meaning": "engrave happiness"
  },
  "Solace": {
    "chinese": "锼蕾丝",
    "pinyin": "sōu lěi sī",
    "meaning": "engrave happy silk"
  },
  "Solus": {
    "chinese": "锼罗丝",
    "pinyin": "sōu luó sī",
    "meaning": "engrave + net + silk"
  },
  "Sonia": {
    "chinese": "锼霓雅",
    "pinyin": "sōu ní yǎ",
    "meaning": "engrave, rainbow, elegance"
  },
  "Sophia": {
    "chinese": "索菲雅",
    "pinyin": "suǒ fēi yǎ",
    "meaning": "search for fragrant elegance"
  },
  "Sophie": {
    "chinese": "锼菲",
    "pinyin": "sōu fēi",
    "meaning": "engrave, fragrant"
  },
  "Sparks": {
    "chinese": "丝琶尔克丝",
    "pinyin": "sī pā ěr kè sī",
    "meaning": "silk + pipa + you (classical) + overcome + silk"
  },
  "Star": {
    "chinese": "丝塔尔",
    "pinyin": "sī tǎ ěr",
    "meaning": "silk + pagoda + you (classical)"
  },
  "Starria": {
    "chinese": "斯塔丽雅",
    "pinyin": "sī tǎ lì yǎ",
    "meaning": "this tower beautiful elegance"
  },
  "Stella": {
    "chinese": "斯特拉; 丝特拉",
    "pinyin": "sī tè lā; sī tè lā",
    "meaning": "this special pull, official transliteration; silk, unique, pull"
  },
  "Stephanie": {
    "chinese": "丝特佛霓",
    "pinyin": "sī tè fó ní",
    "meaning": "silk + unique + seems + rainbow"
  },
  "Stevie": {
    "chinese": "丝特碧",
    "pinyin": "sī tè bì",
    "meaning": "silk, special, jade"
  },
  "Sugar": {
    "chinese": "秀格",
    "pinyin": "xiù gé",
    "meaning": "elegance style"
  },
  "Suiren": {
    "chinese": "睟仁",
    "pinyin": "suì rén",
    "meaning": "bright eyes, kindness"
  },
  "Suki": {
    "chinese": "苏琪",
    "pinyin": "sū qí",
    "meaning": "revive, fine jade"
  },
  "Summer": {
    "chinese": "洒默",
    "pinyin": "sǎ mò",
    "meaning": "unrestrained/carefree, silence"
  },
  "Sunny": {
    "chinese": "萨霓",
    "pinyin": "sà ní",
    "meaning": "bodhisattva rainbow"
  },
  "Sya": {
    "chinese": "希雅",
    "pinyin": "xī yǎ",
    "meaning": "hopeful elegance"
  },
  "Tabitha": {
    "chinese": "塔碧莎",
    "pinyin": "tǎ bì shā",
    "meaning": "pagoda + jade + sedge grass/fern"
  },
  "Takara": {
    "chinese": "达卡拉",
    "pinyin": "dá kǎ lā",
    "meaning": "reach + ka + pull"
  },
  "Tashina": {
    "chinese": "达希娜",
    "pinyin": "dá xī nà",
    "meaning": "reach hope grace"
  },
  "Taylor": {
    "chinese": "泰勒",
    "pinyin": "tài lè",
    "meaning": "official transliteration: peaceful, rein in"
  },
  "Teddy": {
    "chinese": "泰抵",
    "pinyin": "tài dǐ",
    "meaning": "grand resistance"
  },
  "Tenma": {
    "chinese": "天玛",
    "pinyin": "tiān mǎ",
    "meaning": "Heavenly agate"
  },
  "Tenshi": {
    "chinese": "天士，天使",
    "pinyin": "tiān shì，tiān shǐ",
    "meaning": "heavenly warrior, angel"
  },
  "Tensu": {
    "chinese": "天苏",
    "pinyin": "tiān sū",
    "meaning": "Heavenly revival"
  },
  "Thanh": {
    "chinese": "糖",
    "pinyin": "táng",
    "meaning": "sugar"
  },
  "Thea": {
    "chinese": "蒂雅",
    "pinyin": "dì yǎ",
    "meaning": "elegant flower stem"
  },
  "Theo": {
    "chinese": "袭偶",
    "pinyin": "xí ǒu",
    "meaning": "attack, occasionally"
  },
  "Theodore": {
    "chinese": "袭偶躲",
    "pinyin": "xí ǒu duǒ",
    "meaning": "attack, occasionally, hide/dodge"
  },
  "Tiara": {
    "chinese": "缇雅拉",
    "pinyin": "tì yǎ lā",
    "meaning": "red silk + elegant + pulls"
  },
  "Tiffany": {
    "chinese": "缇茷霓",
    "pinyin": "tí fá ní",
    "meaning": "red/orange silk, dense grass, rainbow"
  },
  "Timothy": {
    "chinese": "麒墨喜",
    "pinyin": "qí mò xǐ",
    "meaning": "male qilin + black ink + happiness"
  },
  "Tintin": {
    "chinese": "婷婷",
    "pinyin": "tíng tíng",
    "meaning": "graceful, graceful"
  },
  "Toddy": {
    "chinese": "塔蒂",
    "pinyin": "tǎ dì",
    "meaning": "pagoda + flower stem"
  },
  "Tracy": {
    "chinese": "特蕾西，特蕾西希",
    "pinyin": "tè lěi xī",
    "meaning": "official transliteration (unique, flower/tree bud, west) ; ours: unique, flower/tree buds, hope"
  },
  "Tres": {
    "chinese": "池蕾丝",
    "pinyin": "chí lěi sī",
    "meaning": "pool, flower/leaf bud, silk"
  },
  "Trixy": {
    "chinese": "特日克希",
    "pinyin": "tè rì kè xī",
    "meaning": "special, sun, overcome, hope"
  },
  "tsukuyumi": {
    "chinese": "初苦幽蜜",
    "pinyin": "chū kǔ yōu mì",
    "meaning": "beginning, bitterness, mysterious, secret (there is no ku in Chinese that has a good meaning; also tried to capture the feeling of Tsukuyomi)"
  },
  "Tulip": {
    "chinese": "图丽谱",
    "pinyin": "tú lì pǔ",
    "meaning": "drawing, beautiful, music score"
  },
  "Ursula": {
    "chinese": "尔璱拉",
    "pinyin": "ěr sè lā",
    "meaning": "you (classical), bright jade, pull"
  },
  "Valentine": {
    "chinese": "芭崚泰恩",
    "pinyin": "bā léng tài ēn",
    "meaning": "fragrant plant, lofty mountain, tranquil, kindness"
  },
  "Vanessa": {
    "chinese": "花妮莎，花内纱",
    "pinyin": "huā ní shā, huā nèi shā",
    "meaning": "flower girl sedge grass/fern; flower inner muslin announce"
  },
  "Vani": {
    "chinese": "芭昵",
    "pinyin": "bā nì",
    "meaning": "fragrant plant + intimate"
  },
  "Vania": {
    "chinese": "芭妮雅",
    "pinyin": "bā nī yǎ",
    "meaning": "fragrant plant, girl, elegant"
  },
  "Vashnya": {
    "chinese": "花是你呀，花事妮雅",
    "pinyin": "huā shì nǐ ya, huā shì nī yǎ",
    "meaning": "you're the flower, flower business graceful and elegant"
  },
  "Veronica": {
    "chinese": "维罗妮卡",
    "pinyin": "wéi luò nī kǎ",
    "meaning": "standard transliteration. means maintain, net, girl, ka (card)"
  },
  "Verrena": {
    "chinese": "芭蕾娜",
    "pinyin": "bā lěi nà",
    "meaning": "fragrant plant, flower/leaf bud, graceful"
  },
  "Vicky": {
    "chinese": "碧琪",
    "pinyin": "bì qí",
    "meaning": "fine jade"
  },
  "Victoria": {
    "chinese": "维多利亚",
    "pinyin": "wéi duó lì yǎ",
    "meaning": "standard transliteration"
  },
  "Vinny": {
    "chinese": "碧妮",
    "pinyin": "bì nī",
    "meaning": "jade girl"
  },
  "Violet": {
    "chinese": "白藕莱特",
    "pinyin": "baī ǒu lái tè",
    "meaning": "white lotus weed unique"
  },
  "Violette": {
    "chinese": "碧藕蕾特",
    "pinyin": "bì ǒu lěi tè",
    "meaning": "jade + lotus + flower bud + special"
  },
  "Vivian": {
    "chinese": "碧碧恩",
    "pinyin": "bì bì ēn",
    "meaning": "jade / jade / kindness"
  },
  "Vivienne": {
    "chinese": "碧碧恩",
    "pinyin": "bì bì ēn",
    "meaning": "jade, jade, kindness"
  },
  "VyVy": {
    "chinese": "碧碧",
    "pinyin": "bì bì",
    "meaning": "jade"
  },
  "Wa": {
    "chinese": "娃",
    "pinyin": "wá",
    "meaning": "baby"
  },
  "Winona": {
    "chinese": "维诺娜",
    "pinyin": "wéi nuò nà",
    "meaning": "maintain promise elegance"
  },
  "Wisteria": {
    "chinese": "维丝特丽雅",
    "pinyin": "wéi sī tè lì yǎ",
    "meaning": "maintain, silk, special, beautiful, elegance"
  },
  "Wuuri": {
    "chinese": "雾丽",
    "pinyin": "wù lì",
    "meaning": "beautiful mist"
  },
  "Ximena": {
    "chinese": "喜璊娜",
    "pinyin": "xǐ mén nà",
    "meaning": "happiness, red jade, graceful (there is no Hee sound in Chinese)"
  },
  "Xochitl": {
    "chinese": "锼琪朵，锼琪特尔",
    "pinyin": "sōu qí duǒ, sōu qí tè ěr",
    "meaning": "engrave, fine jade, blossom; engrave, fine jade, special, you (classical)"
  },
  "Xylia": {
    "chinese": "吉尔拉",
    "pinyin": "jí ěr lā",
    "meaning": "lucky, you, pull"
  },
  "Yana": {
    "chinese": "雅娜",
    "pinyin": "yǎ nà",
    "meaning": "elegant, graceful"
  },
  "Yara": {
    "chinese": "雅辣",
    "pinyin": "yǎ là",
    "meaning": "elegant spice"
  },
  "Yashi": {
    "chinese": "雅希",
    "pinyin": "yǎ xí",
    "meaning": "elegant hope"
  },
  "Yashienne": {
    "chinese": "雅希恩",
    "pinyin": "yǎ xí ēn",
    "meaning": "elegant hope peace"
  },
  "Yasmine": {
    "chinese": "雅丝敏",
    "pinyin": "yǎ sī mǐn",
    "meaning": "elegant, silk, intelligent"
  },
  "Yaya": {
    "chinese": "雅雅",
    "pinyin": "yǎ yǎ",
    "meaning": "elegant, elegant"
  },
  "Yekaterina": {
    "chinese": "叶卡特琳娜",
    "pinyin": "yè kǎ tè lín nà",
    "meaning": "leaf + ka + special, gem, graceful"
  },
  "Yemelin": {
    "chinese": "叶美琳",
    "pinyin": "yè měi lín",
    "meaning": "leaf, beautiful gem"
  },
  "Yen": {
    "chinese": "叶恩",
    "pinyin": "yè ēn",
    "meaning": "leaf, kindness"
  },
  "Yeori": {
    "chinese": "叶藕黎",
    "pinyin": "yè ōu lí",
    "meaning": "leaf, lotus, Dark (Zayne's Li)"
  },
  "Yerimia": {
    "chinese": "叶黎蜜雅",
    "pinyin": "yè lí mì yǎ",
    "meaning": "leaf + Dark (Zayne's Li), honey, elegance"
  },
  "Yessie": {
    "chinese": "叶喜",
    "pinyin": "yè xǐ",
    "meaning": "leaf, happiness"
  },
  "Yochan": {
    "chinese": "优婵",
    "pinyin": "yōu chán",
    "meaning": "excellent, beautiful"
  },
  "Yofie": {
    "chinese": "优菲",
    "pinyin": "yōu fēi",
    "meaning": "exceptional / fragrant"
  },
  "Ysabel": {
    "chinese": "意洒贝尔",
    "pinyin": "yì sǎ bèi ěr",
    "meaning": "intent, carefree, treasure, you (classical)"
  },
  "Yuhaida": {
    "chinese": "玉海达",
    "pinyin": "yù hǎi dá",
    "meaning": "jade ocean + reach"
  },
  "Yuhiro": {
    "chinese": "宇辉柔",
    "pinyin": "yǔ huī róu",
    "meaning": "universe, shining splendor, gentle"
  },
  "Yuki": {
    "chinese": "幼琪 or 玉琪",
    "pinyin": "yòu qí; yù qí",
    "meaning": "young fine jade; fine jade"
  },
  "Yukina": {
    "chinese": "幼琪娜 or 玉琪娜",
    "pinyin": "yòu qí nà or yù qí nà",
    "meaning": "graceful young fine jade or graceful fine jade"
  },
  "Yuko": {
    "chinese": "玉蔻",
    "pinyin": "yù kòu",
    "meaning": "jade cardamom"
  },
  "Yulian": {
    "chinese": "玉莲",
    "pinyin": "yù lián",
    "meaning": "jade lotus"
  },
  "Yuna": {
    "chinese": "玉娜",
    "pinyin": "yù nà",
    "meaning": "jade, graceful"
  },
  "Yuri": {
    "chinese": "玉丽",
    "pinyin": "yù lì",
    "meaning": "jade, beautiful"
  },
  "Zai": {
    "chinese": "宰",
    "pinyin": "zǎi",
    "meaning": "sovereign"
  },
  "Zaphire": {
    "chinese": "杂菲蕾",
    "pinyin": "zá fēi lěi",
    "meaning": "mixed fragrant buds (leaf/flower)"
  },
  "Zara": {
    "chinese": "杂拉",
    "pinyin": "zá lā",
    "meaning": "mixed + pull"
  },
  "Zazie": {
    "chinese": "匝己",
    "pinyin": "zā jǐ",
    "meaning": "encircle self - higher focus on pronunciation"
  },
  "Zech": {
    "chinese": "杰克",
    "pinyin": "jié kè",
    "meaning": "heroic, overcome"
  },
  "Zee": {
    "chinese": "滋，吉",
    "pinyin": "zī, jí",
    "meaning": "grow, luck"
  },
  "Zeina": {
    "chinese": "鰂娜",
    "pinyin": "zéi nà",
    "meaning": "cuttlefish, elegant (sorry no other zei)"
  },
  "Zeph": {
    "chinese": "泽福",
    "pinyin": "zé fú",
    "meaning": "lustrous fortune"
  },
  "Zevan": {
    "chinese": "责湾/万",
    "pinyin": "zé wān",
    "meaning": "duty crescent"
  },
  "Zhaela": {
    "chinese": "鰂拉",
    "pinyin": "zéi lā",
    "meaning": "cuttlefish pull (sorry no other nice zhae/zay sound)"
  },
  "Zia": {
    "chinese": "滋雅",
    "pinyin": "zī yǎ",
    "meaning": "grow, elegance"
  },
  "Zodia": {
    "chinese": "緅蒂雅",
    "pinyin": "zōu dì yǎ",
    "meaning": "purple silk, flower stem, elegance"
  },
  "Zoe Aster": {
    "chinese": "奏𫖮，阿丝特",
    "pinyin": "zòu yǐ, ā sī tè",
    "meaning": "play music + pleasant, a + silk + Unique"
  },
  "Zukhra": {
    "chinese": "珠苦拉",
    "pinyin": "zhū kǔ lā",
    "meaning": "pearl, bitter (sorry, no other ku works), pull"
  },
  "Zy": {
    "chinese": "吉 / 宰",
    "pinyin": "jí / zǎi",
    "meaning": "lucky sovereign"
  },
  "Zyella": {
    "chinese": "吉尔拉",
    "pinyin": "jí ěr lā",
    "meaning": "lucky, you, pull"
  },
  "Zyhia": {
    "chinese": "宰雅",
    "pinyin": "zǎi yǎ",
    "meaning": "elegant sovereign"
  }
}

ā')
                meaning_parts.append("phonetic approximation")
    
    return {
        'chinese': ''.join(chinese_chars),
        'pinyin': ' '.join(pinyin_parts),
        'meaning': ' + '.join(meaning_parts) + ' (phonetic conversion)',
        'source': 'phonetic'
    }

def search_names(query, gender='neutral', limit=10):
    """
    Search for names using fuzzy matching and phonetic conversion
    Returns both exact matches from database and phonetic conversions
    """
    if not query:
        return []
    
    results = []
    
    # First, search in curated database
    matches = process.extract(query, NAMES_DATA.keys(), scorer=fuzz.ratio, limit=limit)
    
    for match_name, score in matches:
        if score >= 60:  # Minimum similarity threshold
            data = NAMES_DATA[match_name]
            results.append({
                'name': match_name,
                'chinese': data['chinese'],
                'pinyin': data['pinyin'],
                'meaning': data['meaning'],
                'score': score,
                'source': 'curated'
            })
    
    # Always add phonetic conversion as an option
    phonetic_result = create_phonetic_conversion(query, gender)
    phonetic_result.update({
        'name': query.title(),
        'score': 55,  # Lower score to indicate it's phonetic
        'source': 'phonetic'
    })
    results.append(phonetic_result)
    
    # Sort by score (curated matches first due to higher scores)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:limit]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()
    gender = request.args.get('gender', 'neutral').strip()
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Validate gender parameter
    if gender not in ['female', 'male', 'neutral']:
        gender = 'neutral'
    
    results = search_names(query, gender, limit)
    return jsonify({
        'query': query,
        'gender': gender,
        'results': results,
        'total_names': len(NAMES_DATA)
    })

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'total_names': len(NAMES_DATA),
        'sample_names': list(NAMES_DATA.keys())[:10]
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
