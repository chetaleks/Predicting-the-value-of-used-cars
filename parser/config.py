MARKS = ["vaz", "aurus", "belgee", "uaz", "gaz", "moscvich", "solaris", "ig", "sollers", "ravon", "evolute",
         "tagaz", "promo_auto", "doninvest", "dw_hower", "derways", "ambertruck", "smz", "kanonir", "kombat",
         "vortex", "xcite", "zil", "zis", "audi", "abarth", "ac", "acura", "adler", "aito", "swm", "avatr",
         "foton", "trumpchi", "hawtai", "icar", "im_motors", "jmc", "aiways", "aixam", "alfa_romeo", "alpina", 
         "alpine", "am_general", "arcfox", "aro", "asia", "aston_martin", "austin", "autobianchi", 
         "baic", "bajaj", "baltijas_dzips", "baojun", "baw", "bentley", "bmw", "bestune", "borgward", "brilliance", "bugatti",
         "buick", "byd", "cadillac", "chana", "changan", "changfeng", "chevrolet", "chery", "chrysler", "ciimo", "citroen",
         "coda", "cupra", "dacia", "dadi", "daewoo", "daihatsu", "daimler", "datsun", "dayun", "delage", "delorean", "denza",
         "dodge", "dongfeng", "ds", "eagle", "enovate", "everus", "excalibur", "exeed", "facel_vega", "faw", "ferrari",
         "fiat", "ford", "forthing", "fso", "gac", "aion", "geely", "haval", "genesis", "gmc", "gp", "great_wall",
         "hafei", "haima", "hanteng", "hiphi", "honda", "hongqi", "hozon", "huanghai", "hudson", "hummer", "hyundai",
         "ineos", "infiniti", "innocenti", "iran_khodro", "isuzu", "jac", "jaecoo", "jaguar", "jeep", "jetour",
         "jetta", "jidu", "jinbei", "jmev", "kaiyi", "kawei", "kgm", "kia", "knewstar", "koenigsegg", "lamborghini", 
         "lancia", "land_rover", "landwind", "leapmotor", "levc", "lexus", "liebao", "lifan", "lincoln", "livan",
         "lixiang", "lotus", "lucid", "luxeed", "luxgen", "lynk_co", "m_hero", "mahindra", "maple", "maserati",
         "maxus", "maybach", "mazda", "mclaren", "mercedes", "mercury", "metrocab", "mg", "mini", "mitsubishi",
         "mitsuoka", "morgan", "nio", "nissan", "oldsmobile", "omoda", "opel", "ora", "oshan", "oting", "packard",
         "pagani", "peugeot", "plymouth", "polar_stone_jishi", "polestar", "pontiac", "porsche", "proton", "puch",
         "qingling", "qoros", "ram", "renault", "samsung", "rising_auto", "rivian", "roewe", "rolls_royce", "rover",
         "rox", "saab", "saturn", "scion", "seat", "seres", "shuanghuan", "simca", "skoda", "skywell", "smart", 
         "soueast", "ssang_yong", "stelato", "steyr", "subaru", "suzuki", "tank", "tata", "tatra", "tesla", "tianma",          
         "tianye", "toyota", "trabant", "vauxhall", "venucia", "vgv", "volkswagen", "volvo", "voyah", "wanderer", "wartburg", 
         "luaz", "zaz", "zx", "zotye", "zeekr", "xpeng", "xinkai", "xiaomi", "wuling", "willis", "wey", "weltmeister"
        ]

PARSED_MARKS = ['abarth', 'ac', 'acura', 'adler', 'aion', 'aito', 'aiways', 'aixam', 'alfa_romeo', 'alpina', 'alpine', 
                 'ambertruck', 'arcfox', 'aro', 'asia', 'aston_martin', 'audi', 'aurus', 'austin', 'autobianchi', 'avatr', 
                 'baic', 'bajaj', 'baltijas_dzips', 'baojun', 'baw', 'belgee', 'bentley', 'bestune', 'bmw', 'borgward', 
                 'brilliance', 'bugatti', 'buick', 'byd', 'cadillac', 'chana', 'changan', 'changfeng', 'chery', 'chevrolet', 
                 'chrysler', 'ciimo', 'citroen', 'coda', 'cupra', 'dacia', 'dadi', 'daewoo', 'daihatsu', 'daimler', 'datsun', 
                 'dayun', 'delage', 'delorean', 'denza', 'derways', 'dodge', 'dongfeng', 'doninvest', 'ds', 'dw_hower', 'eagle', 
                 'enovate', 'everus', 'evolute', 'excalibur', 'exeed', 'facel_vega', 'faw', 'ferrari', 'fiat', 'ford', 'forthing', 
                 'foton', 'fso', 'gac', 'gaz', 'geely', 'genesis', 'gmc', 'great_wall', 'hafei', 'haima', 'hanteng', 'haval', 
                 'hawtai', 'hiphi', 'honda', 'hongqi', 'hozon', 'huanghai', 'hudson', 'hummer', 'hyundai', 'icar', 'ig', 'im_motors', 
                 'ineos', 'infiniti', 'innocenti', 'iran_khodro', 'isuzu', 'jac', 'jaecoo', 'jaguar', 'jeep', 'jetour', 'jetta', 
                 'jidu', 'jinbei', 'jmc', 'jmev', 'kaiyi', 'kanonir', 'kawei', 'kgm', 'kia', 'knewstar', 'koenigsegg', 
                 'lamborghini', 'lancia', 'landwind', 'land_rover', 'leapmotor', 'levc', 'lexus', 'liebao', 'lifan', 'lincoln', 
                 'livan', 'lixiang', 'lotus', 'luaz', 'lucid', 'luxeed', 'luxgen', 'lynk_co', 'mahindra', 'maple', 'maserati', 
                 'maxus', 'maybach', 'mazda', 'mclaren', 'mercedes', 'mercury', 'metrocab', 'mg', 'mini', 'mitsubishi', 'mitsuoka', 
                 'morgan', 'moscvich', 'm_hero', 'nio', 'nissan', 'oldsmobile', 'omoda', 'opel', 'ora', 'oshan', 'oting', 'packard', 
                 'pagani', 'peugeot', 'plymouth', 'polar_stone_jishi', 'polestar', 'pontiac', 'porsche', 'promo_auto', 'proton', 
                 'puch', 'qingling', 'qoros', 'ram', 'ravon', 'renault', 'rising_auto', 'rivian', 'roewe', 'rolls_royce', 'rover', 
                 'rox', 'saab', 'samsung', 'saturn', 'scion', 'seat', 'seres', 'shuanghuan', 'simca', 'skoda', 'skywell', 'smart', 
                 'smz', 'solaris', 'sollers', 'soueast', 'ssang_yong', 'stelato', 'steyr', 'subaru', 'suzuki', 'swm', 'tagaz', 'tank', 
                 'tata', 'tatra', 'tesla', 'tianma', 'tianye', 'toyota', 'trabant', 'trumpchi', 'uaz', 'vauxhall', 'vaz', 'venucia', 
                 'vgv', 'volkswagen', 'volvo']

HEADERS = '''
accept: */*
accept-encoding: gzip, deflate, br, zstd
accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
content-length: 74
content-type: application/json
cookie: cookie
origin: https://auto.ru
priority: u=1, i
referer: https://auto.ru/sankt-peterburg/cars/all/?page=2
sec-ch-ua: "Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: same-origin
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
x-client-app-version: 318.0.15977935
x-client-date: 1740592028943
x-csrf-token: a220bba8ba2dfc0b5c14a527160980c17b90fd0cfc8b65a3
x-page-request-id: 99e8b01f04ad0c8364a4a1f4e9043808
x-requested-with: XMLHttpRequest
x-retpath-y: https://auto.ru/sankt-peterburg/cars/all/?page=2
x-yafp: {"a1":"WJlxceAHcDK+QA==;0","a2":"F28ntZRy7Olx2ICA6Zx/r8VSuARIZQ==;1","a3":"WRU28EdhoSG28DCMubIVug==;2","a4":"Pg8Ti8J291f2JsUtLEkzu3Dz9LqBfArnut0L5tN7ZhaGFg==;3","a5":"Pv/TbLQ/Yg6WXg==;4","a6":"PkE=;5","a7":"LVg7NWEWAcDy3w==;6","a8":"kFPj4dzirJk=;7","a9":"Jweeg62jT4dVEQ==;8","b1":"fi/p+4Bvjx8=;9","b2":"1fYQPumW1wH7zg==;10","b3":"FoeM2tfmCmrYbw==;11","b4":"amZZI2iOU3Q=;12","b5":"ZDihQyy76yaeCQ==;13","b6":"bbwNEJJ3yZ+RRQ==;14","b7":"lmu8Pvnp2wgafA==;15","b8":"asMllTAxDBding==;16","b9":"FWTAXFjxtUx52g==;17","c1":"BQv1sA==;18","c2":"wSEGTdaCf8xVZiI13fEVar/3;19","c3":"VqI6M4l6f37ECRoK1OjHgl6W;20","c4":"huE/a33GuPU=;21","c5":"VA6l4ZIVL1w=;22","c6":"s+IBxQ==;23","c7":"5ZINMDWiTyc=;24","c8":"kXA=;25","c9":"jukKoVRJQhI=;26","d1":"4/KxVG5eAVk=;27","d2":"q+c=;28","d3":"o0oFJLTAcPnR5g==;29","d4":"mLTYiR30Kgg=;30","d5":"tnYmt/HEtWz1og==;31","d7":"WEOPfu1E8cc=;32","d8":"AQmheMRfU/XgW15nALI1CpRsBb6jXlTYWfg=;33","d9":"JOTPQYBQD5I=;34","e1":"xpoHFGbqW3pfuw==;35","e2":"JlgY3PMqNlA=;36","e3":"uI3WYLQj5Kk=;37","e4":"BxKEzCWjZoA=;38","e5":"Co1TKlAiD4H+Dw==;39","e6":"XWxdYo/+sgU=;40","e7":"63taTSXogFJdxA==;41","e8":"TVN3Gyc2GwU=;42","e9":"dIDPFy4GXvM=;43","f1":"zavfWz+4Eg8XUA==;44","f2":"AIq7bOefc+U=;45","f3":"YbkVQZaBUIfFvQ==;46","f4":"YrYo20Uil+w=;47","f5":"T2btfeje/2RFRg==;48","f6":"GLkJ6mu6NEurnw==;49","f7":"S1YRZw7afNuoyg==;50","f8":"/6MCfwPAdRpZ7Q==;51","f9":"DUPXkHrquHg=;52","g1":"3YHarhg9cZYsiA==;53","g2":"RBMQ2XYwaTtoVg==;54","g3":"yhffEvrltDo=;55","g4":"bfXM0YOFqOmwpw==;56","g5":"D5Rkxikotfs=;57","g6":"gBm/c/nDMTA=;58","g7":"EoEE5cM0oKo=;59","g8":"jYFc++se0oM=;60","g9":"gNMXJSksjo8=;61","h1":"W5OHLYcoYyhB2A==;62","h2":"Y94gU/pleCNDtw==;63","h3":"NwpeDXiSBBqrOg==;64","h4":"CudcpDp6VYuBNg==;65","h5":"u2pC5/9zcnU=;66","h6":"TuOxEz4nx+eaMw==;67","h7":"d1+xDkFa8XLchBzIBcs4HjzHn/cBtloTew7bhZQAUn1HK9/m;68","h8":"fRG+Pf4DMPmhqg==;69","h9":"wbspB2jMgSAMtw==;70","i1":"q0RXft/wS/A=;71","i2":"VPIAVjGc4/o6NQ==;72","i3":"xoZ/jpDduLURrw==;73","i4":"nIeum0gGpye31g==;74","i5":"nKPNam2Ub3BnuQ==;75","z1":"aGG/19XyMnQLnR2oXbBzhTHHMc5TMOMiiyzTbc5vyfsZELuKzXX1nkQB9Au4ltgNv1IR+Jt5Iy0w8gtmJx7I1Q==;76","z2":"JKr9v8X/BC9qcfdssXpF07Y/C115flo0DVesw0g+6izhTKL81IjMLKV6mEGuFJAzgy1XFUA2veZ5FogIBM+6yQ==;77","y2":"QJe/WTmN/FDlsA==;78","y3":"e+wcBM9t167L5w==;79","y6":"sz1JHN86Gr/RZA==;80","y8":"VlMbVGtosgrN+g==;81","x4":"0Qyv4xfbxOwH3g==;82","z4":"bv2bd8OxIvTYzA==;83","z6":"cQa8IEuJS9sWR/w3;84","z7":"ANcpKOYQwM6IP+A2;85","z8":"Q3NlkrBMjMH5464r;86","z9":"iYojhuXVkDuKKOJi;87","y1":"QitrX9C+0K4wyMIT;88","y4":"MxDDN/FNwaibwWEY;89","y5":"6Lwy5B2YV1jCSvHsF0I=;90","y7":"fPha/wc0UuW7aY/Y;91","y9":"5YKoAfGQiv5ZuGd10zI=;92","y10":"/YntcORfvDtqHjDnYbM=;93","x1":"kMguLqmOYtOlSgRV;94","x2":"UBilbCrfkPKfKkHriTs=;95","x3":"WVp693xRdiHUBWkD;96","x5":"wotSrDKfK81eOuOv;97","z3":"/lFMSvO6Tuk7O6eYrSQ=;98","z5":"rPXcuDZ2ec8Py27qnIw=;99","v":"6.3.1","pgrdt":"H77FsJKrVnenG0Pto6BjEmvV3L8=;100","pgrd":"6w0cMZlW7zi1hhXGNwtp63ScLjhmUIiagfgW+56tg21xW7jrkPSCYPN06xGFsYkFK2gTjgNfDyoc2D2MAOA/pswltXkFLe6kUMt3pqFBK7TlZLUVO7XIUcT2K5dxw2cGReOtFidkw6LPKLkF6QDy0yNuxt4/pVdozqVrDRFq/RnSzHMFVsNLtrzCcRGDljn8iM4v1LRj8WtxzYjhzglpjNtj1Y0="}'''.strip().split("\n")

PARAMS = {
  "section": "all",
  "category": "cars",
  "catalog_filter": [
    {
      "mark": "TRUMPCHI",
      "model": "E9"
    }
  ],
  "output_type": "list",
  "geo_id": [
  ]
}

URL = "https://auto.ru/-/ajax/desktop-search/listing/"

DICT_HEADERS = {}
for header in HEADERS:
    key, value = header.split(': ')
    DICT_HEADERS[key] = value