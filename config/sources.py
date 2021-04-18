# pages can be ignored via timestamp or range of timestamps, eg if page didn't change in consecutive days or there was a page error
# encoding can be defined like timestamps
news_sources = [
    {
        'site': 'news.google.pt',
        'from': '20051124000000'
    },
    {
        'site': 'publico.pt',
        'special': {'20100910150634': '?fl=1', '20110703150815': '?mobile=no'},
        'ignore': ['19961013180344', '19990421171920-20001203173200']
    },
    {
        'site': 'portugaldiario.iol.pt',
        'ignore': ['20001119134000', '20001202055200', '20010202072300', '20050325075505', '20050828053247'],
        'to': '20100626141610'  # becomes a redirect to tvi24 after
    },
    {
        'site': 'jn.pt',
        'encoding': {
            '20040605042739-20080314182313': 'utf-8'
        },
        'ignore': [
            '20011014000211', '20011103001652', '20011107005932', '20011107010100', '20011108003840', '20011108010152', '20011116002347', '20011116002419', '20011117011734', '20011128004742',
            '20021125205745', '20030218052808', '20030407162709', '20030624151104', '20031030000220', '20031214025515', '20031225105031', '20040612021612', '20040616183544', '20081022054919',
            '20090926013934', '20091218091852', '20060826115813', '20060826202309', '20080215063034', '20081022054919', '20081022055157', '20081022063817', '20090522005146',  '20090623195309',
            '20100606104209', '20110621150208', '20131115102830', '20100706140103', '20150416191052-20150505170210'
        ]
    },
    {
        'site': 'expresso.pt',
        'ignore': [
            '20000303215339', '20000304003451', '20000511112040', '20000614221642-20000815100152', '20001019034724-20010519195029', '20010924001343', '20010930112729', '20011002002004',
            '20011014233012', '20010930234309', '20011021145713', '20011022031247', '20011028041447', '20011029044539', '20011104005540', '20011105005759', '20011111012646', '20011112013327',
            '20011114004021', '20011125030751', '20011126050422', '20011202173222', '20011209175945', '20030327225541', '20030408155413', '20011021154458', '20011022040823', '20011028212409',
            '20011029054219', '20011104014656', '20011105022015', '20011111014527', '20011114010516', '20011125161129', '20011202184517', '20011209191928', '20011023013327', '20011104140315',
            '20011106011738', '20011111140017', '20011115021401', '20011116000618', '20011116080231', '20040606233331-20040612075222', '20040626033600-20040701060606', '20040724050140',
            '20040725065449', '20051223054221', '20070614005353', '20040903045728-20041215022252', '20050401233212-20050621185523', '20051124222130', '20051125040706', '20051225095630-20051231182511',
            '20090925190706-20091218062538', '20060102013519', '20060103082829', '20060108135453', '20060101042421', '20060102045952', '20060101123534', '20060102081843', '20091218182923',
            '20060101153422', '20060102113344', '20060101172409', '20060102153620', '20060101201140', '20060102173036', '20060101233307', '20060102205258', '20060102234035', '20061023050337',
            '20070614005353', '20090628235239'
        ]
    },
    {
        'site': 'dn.pt',
        'ignore': ['19971210080753-20011217081100',  # use the first alternative source
                   '20011001070732-20011216025543',  # period where it redirects to lusomundo, which was only archived in 2005
                   '20020117114627-20040618191302',  # use the second alternative source
                   # redirected to sapo.pt
                   '20041112090609', '20041113094530', '20041124092713', '20041126011101', '20050204095321', '20050206084348', '20050331091414',
                   '20041126085901', '20050204233149', '20050206130903', '20050401090655', '20050419080718', '20050420085351', '20060705062020',
                   '20060820071734', '20060825232258', '20060826050346', '20060826185341',

                   # not found
                   '20110121225541',

                   # use the third alternative source
                   '20110522215801-20151013180422'
                   ]
    },
    {
        # it's best to do as a separate source, because special would force the main page's timestamp
        # onto a different page, and the capture dates for the special page might differ from the main's
        'site': 'dn.pt',
        'path': '/pri/sintpri.htm',
        'from': '19971210080753',
        'to': '20011001001039',  # after this and until 2002 it's the 30/09 edition repeated everytime
        'target': 'dn.pt'  # store as if it was this one
    },
    {
        'site': 'dn.sapo.pt',
        'path': '/homepage/homepage.asp',
        'from': '20020117114627',
        'to': '20040618191302',
        'target': 'dn.pt'  # store as if it was this one
    },
    {
        'site': 'dn.pt',
        'path': '/inicio/default.aspx',
        'from': '20110522215801',
        'to': '20151013180422',
        'target': 'dn.pt',  # store as if it was this one
        'ignore': ['20110621150217']
    },
    {
        'site': 'aeiou.pt',
        'from': 19990420195435,  # no news before
        'ignore': [
            '20010202085000-20010202141600',  # weird page

            # alternate version contained in iframe
            '20020327025158', '20020601110324', '20020602020939', '20020604020102', '20020724072703', '20020802120758', '20020926150515',
            '20021120082141', '20021127043332', '20030208133441-20030422003232', '20030522224359-20030807213119', '20031001004649',

            # empty
            '20071217030135',

            # below
            '20020327025158-20031001043355', '20031001043355-20070308030604'
        ]
    },
    {
        'site': 'aeiou.pt',
        'path': '/primeira/index.php',
        'from': 20020327025158,
        'to': 20031001043355,
        'target': 'aeiou.pt'
    },
    {
        'site': 'aeiou.pt',
        'path': '/red/primeira/index.php',
        'from': 20031001043355,
        'to': 20070308030604,
        'target': 'aeiou.pt'
    },
    {
        'site': 'noticias.sapo.pt',
        'ignore': [
            '20020802101821', '20050212045123',  # empty/wrong
            '20070225131122-20080222185009'  # seems like it's not archived
        ],
        'encoding': {
             '20051027031535-20070217132649': 'utf-8'
        },
    },
    {
        # "independent" era
        'site': 'diariodigital.pt',
        'from': 20010301220302,  # error pages before
        'to': 20031027120557,
        'ignore': [
            '20020720131716',  # empty
        ]
    },
    {
        # sapo era
        'site': 'diariodigital.sapo.pt',
        'from': 20031213054017,
        'ignore': [
            '20050712082156', '20070611173339', '20071006042355', '20080213190631-20081022053150', '20081022061528',  # redirect to sapo pesquisa
        ],
        'target': 'diariodigital.pt'
    },
    {
        'site': 'tsf.pt',
        'to': 20080314173841,
        'ignore': [
            '20001204045200',  # error
            '20020402122419',  # redirects
            '20020802231431-20080319163335',  # lusomundo version below
        ]
    },
    {
        'site': 'http://www.tsf.pt:80',
        'path': '/especial_portugal_aut.asp',
        'target': 'tsf.pt',
        'from': 20011228150549,
        'to': 20011228150549
    },
    {
        'site': 'http://www.tsf.pt:80',
        'path': '/online/primeira/default.asp',
        'target': 'tsf.pt',
        'from': 20020802231431,
        'to': 20080314173841,
        'ignore': [
            # empty pages
            '20041114052014-20041116010600', '20050213011222', '20050604024827', '20050627014838', '20050629005259',
            '20050901033111', '20050901071740', '20051031084636', '20051125024744', '20070202022827', '20070822233328',
            '20071212170455'
        ]
    },
    {
        'site': 'http://www.tsf.pt',
        'path': '/paginainicial',
        'target': 'tsf.pt',
        'from': 20080523145202,
        'ignore': [
            # errors
            '20091218192658', '20100805222602', '20110128061743', '20110621151454', '20120922151553', '20110128073836',
            '20110520012522', '20110621155548', '20120126082845'
        ]
    },
    {
        'site': 'ultimahora.publico.pt',
        'to': 20090925042626,  # redirects to main publico thereafter
        'ignore': [
            # below
            '19991127135635-20001018231646'
        ]
    },
    {
        'site': 'http://ultimahora.publico.pt:80',
        'path': '/geral.htm',
        'target': 'ultimahora.publico.pt',
        'to': 20001019034116
    },
    {
        # first frame of same page
        'site': 'http://ultimahora.publico.pt:80',
        'path': '/barra-central.asp',
        'target': 'ultimahora.publico.pt',
        'to': 20001019034116
    },

    {'site': 'sabado.pt'},
    {'site': 'iol.pt'},
    {'site': 'sicnoticias.sapo.pt'},
    {'site': 'rtp.pt'},
    {'site': 'visao.sapo.pt'},
    {'site': 'sol.sapo.pt'},
    {'site': 'tvi24.iol.pt'},

    {'site': 'destak.pt'},
    {'site': 'sapo.pt'},
    # {'site': 'cmjornal.pt'},
    # {'site': 'cmjornal.xl.pt'},
    {'site': 'ionline.pt'},
    {'site': 'lux.iol.pt'},
    {'site': 'meiosepublicidade.pt'},
    {'site': 'oprimeirodejaneiro.pt', 'to': '20071231235959'},

    # regional
    {'site': 'dnoticias.pt'},

    # musica
    {'site': 'blitz.pt'},

    # economia
    {'site': 'dinheirovivo.pt'},
    {'site': 'jornaldenegocios.pt'},
    {'site': 'economico.sapo.pt'},

    # desporto
    {'site': 'abola.pt'},
    {'site': 'ojogo.pt'},
    {'site': 'maisfutebol.iol.pt'},
    {'site': 'record.pt'},

    # informatica
    {'site': 'exameinformatica.clix.pt'},
    {'site': 'pcguia.pt'},

    # {'site': '24.sapo.pt'},  # starts 2015
    {'site': 'observador.pt'},  # starts 2013
]
