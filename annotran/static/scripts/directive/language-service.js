'use strict';
function langListFactory() {
    var langList = {};
    var languages = [
        {
            id: '1',
            name: 'Afrikaans',
            description: '',
            comment: ''
        },
        {
            id: '2',
            name: 'Albanian',
            description: '',
            comment: ''
        },
        {
            id: '3',
            name: 'Amharic',
            description: '',
            comment: ''
        },
        {
            id: '4',
            name: 'Arabic',
            description: '',
            comment: ''
        },
        {
            id: '5',
            name: 'Armenian',
            description: '',
            comment: ''
        },
        {
            id: '6',
            name: 'Azerbaijani',
            description: '',
            comment: ''
        },
        {
            id: '7',
            name: 'Basque',
            description: '',
            comment: ''
        },
        {
            id: '8',
            name: 'Belarusian',
            description: '',
            comment: ''
        },
        {
            id: '9',
            name: 'Bengali',
            description: '',
            comment: ''
        },
        {
            id: '10',
            name: 'Bosnian',
            description: '',
            comment: ''
        },
        {
            id: '11',
            name: 'Bulgarian',
            description: '',
            comment: ''
        },
        {
            id: '12',
            name: 'Catalan',
            description: '',
            comment: ''
        },
        {
            id: '13',
            name: 'Cebuano',
            description: '',
            comment: ''
        },
        {
            id: '14',
            name: 'Chichewa',
            description: '',
            comment: ''
        },
        {
            id: '15',
            name: 'Chinese',
            description: '',
            comment: ''
        },
        {
            id: '16',
            name: 'Corsican',
            description: '',
            comment: ''
        },
        {
            id: '17',
            name: 'Croatian',
            description: '',
            comment: ''
        },
        {
            id: '18',
            name: 'Czech',
            description: '',
            comment: ''
        },
        {
            id: '19',
            name: 'Danish',
            description: '',
            comment: ''
        },
        {
            id: '20',
            name: 'Dutch',
            description: '',
            comment: ''
        },
        {
            id: '21',
            name: 'English',
            description: '',
            comment: ''
        },
        {
            id: '22',
            name: 'Esperanto',
            description: '',
            comment: ''
        },
        {
            id: '23',
            name: 'Estonian',
            description: '',
            comment: ''
        },
        {
            id: '24',
            name: 'Filipino',
            description: '',
            comment: ''
        },
        {
            id: '25',
            name: 'Finnish',
            description: '',
            comment: ''
        },
        {
            id: '26',
            name: 'French',
            description: '',
            comment: ''
        },
        {
            id: '27',
            name: 'Frisian',
            description: '',
            comment: ''
        },
        {
            id: '28',
            name: 'Galician',
            description: '',
            comment: ''
        },
        {
            id: '29',
            name: 'Georgian',
            description: '',
            comment: ''
        },
        {
            id: '30',
            name: 'German',
            description: '',
            comment: ''
        },
        {
            id: '31',
            name: 'Greek',
            description: '',
            comment: ''
        },
        {
            id: '32',
            name: 'Gujarati',
            description: '',
            comment: ''
        },
        {
            id: '33',
            name: 'Haitian Creole',
            description: '',
            comment: ''
        },
        {
            id: '34',
            name: 'Hausa',
            description: '',
            comment: ''
        },
        {
            id: '35',
            name: 'Hawaiian',
            description: '',
            comment: ''
        },
        {
            id: '36',
            name: 'Hebrew',
            description: '',
            comment: ''
        },
        {
            id: '37',
            name: 'Hindi',
            description: '',
            comment: ''
        },
        {
            id: '38',
            name: 'Hmong',
            description: '',
            comment: ''
        },
        {
            id: '39',
            name: 'Hungarian',
            description: '',
            comment: ''
        },
        {
            id: '40',
            name: 'Icelandic',
            description: '',
            comment: ''
        },
        {
            id: '41',
            name: 'Igbo',
            description: '',
            comment: ''
        },
        {
            id: '42',
            name: 'Indonesian',
            description: '',
            comment: ''
        },
        {
            id: '43',
            name: 'Irish',
            description: '',
            comment: ''
        },
        {
            id: '44',
            name: 'Italian',
            description: '',
            comment: ''
        },
        {
            id: '45',
            name: 'Japanese',
            description: '',
            comment: ''
        },
        {
            id: '46',
            name: 'Javanese',
            description: '',
            comment: ''
        },
        {
            id: '47',
            name: 'Kannada',
            description: '',
            comment: ''
        },
        {
            id: '48',
            name: 'Kazakh',
            description: '',
            comment: ''
        },
        {
            id: '49',
            name: 'Khmer',
            description: '',
            comment: ''
        },
        {
            id: '50',
            name: 'Korean',
            description: '',
            comment: ''
        },
        {
            id: '51',
            name: 'Kurdish (Kurmanji)',
            description: '',
            comment: ''
        },
        {
            id: '52',
            name: 'Kyrgyz',
            description: '',
            comment: ''
        },
        {
            id: '53',
            name: 'Lao',
            description: '',
            comment: ''
        },
        {
            id: '54',
            name: 'Latin',
            description: '',
            comment: ''
        },
        {
            id: '55',
            name: 'Latvian',
            description: '',
            comment: ''
        },
        {
            id: '56',
            name: 'Lithuanian',
            description: '',
            comment: ''
        },
        {
            id: '57',
            name: 'Luxembourgish',
            description: '',
            comment: ''
        },
        {
            id: '58',
            name: 'Macedonian',
            description: '',
            comment: ''
        },
        {
            id: '59',
            name: 'Malagasy',
            description: '',
            comment: ''
        },
        {
            id: '60',
            name: 'Malay',
            description: '',
            comment: ''
        },
        {
            id: '61',
            name: 'Malayalam',
            description: '',
            comment: ''
        },
        {
            id: '62',
            name: 'Maltese',
            description: '',
            comment: ''
        },
        {
            id: '63',
            name: 'Maori',
            description: '',
            comment: ''
        },
        {
            id: '64',
            name: 'Marathi',
            description: '',
            comment: ''
        },
        {
            id: '65',
            name: 'Mongolian',
            description: '',
            comment: ''
        },
        {
            id: '66',
            name: 'Myanmar (Burmese)',
            description: '',
            comment: ''
        },
        {
            id: '67',
            name: 'Nepali',
            description: '',
            comment: ''
        },
        {
            id: '68',
            name: 'Norwegian',
            description: '',
            comment: ''
        },
        {
            id: '69',
            name: 'Pashto',
            description: '',
            comment: ''
        },
        {
            id: '70',
            name: 'Persian',
            description: '',
            comment: ''
        },
        {
            id: '71',
            name: 'Polish',
            description: '',
            comment: ''
        },
        {
            id: '72',
            name: 'Portuguese',
            description: '',
            comment: ''
        },
        {
            id: '73',
            name: 'Punjabi',
            description: '',
            comment: ''
        },
        {
            id: '74',
            name: 'Romanian',
            description: '',
            comment: ''
        },
        {
            id: '75',
            name: 'Russian',
            description: '',
            comment: ''
        },
        {
            id: '76',
            name: 'Samoan',
            description: '',
            comment: ''
        },
        {
            id: '77',
            name: 'Scots Gaelic',
            description: '',
            comment: ''
        },
        {
            id: '78',
            name: 'Serbian',
            description: '',
            comment: ''
        },
        {
            id: '79',
            name: 'Sesotho',
            description: '',
            comment: ''
        },
        {
            id: '80',
            name: 'Shona',
            description: '',
            comment: ''
        },
        {
            id: '81',
            name: 'Sindhi',
            description: '',
            comment: ''
        },
        {
            id: '82',
            name: 'Sinhala',
            description: '',
            comment: ''
        },
        {
            id: '83',
            name: 'Slovak',
            description: '',
            comment: ''
        },
        {
            id: '84',
            name: 'Slovenian',
            description: '',
            comment: ''
        },
        {
            id: '85',
            name: 'Somali',
            description: '',
            comment: ''
        },
        {
            id: '86',
            name: 'Spanish',
            description: '',
            comment: ''
        },
        {
            id: '87',
            name: 'Sundanese',
            description: '',
            comment: ''
        },
        {
            id: '88',
            name: 'Swahili',
            description: '',
            comment: ''
        },
        {
            id: '89',
            name: 'Swedish',
            description: '',
            comment: ''
        },
        {
            id: '90',
            name: 'Tajik',
            description: '',
            comment: ''
        },
        {
            id: '91',
            name: 'Tamil',
            description: '',
            comment: ''
        },
        {
            id: '92',
            name: 'Telugu',
            description: '',
            comment: ''
        },
        {
            id: '93',
            name: 'Thai',
            description: '',
            comment: ''
        },
        {
            id: '94',
            name: 'Turkish',
            description: '',
            comment: ''
        },
        {
            id: '95',
            name: 'Ukrainian',
            description: '',
            comment: ''
        },
        {
            id: '96',
            name: 'Urdu',
            description: '',
            comment: ''
        },
        {
            id: '97',
            name: 'Uzbek',
            description: '',
            comment: ''
        },
        {
            id: '98',
            name: 'Vietnamese',
            description: '',
            comment: ''
        },
        {
            id: '99',
            name: 'Welsh',
            description: '',
            comment: ''
        },
        {
            id: '100',
            name: 'Xhosa',
            description: '',
            comment: ''
        },
        {
            id: '101',
            name: 'Yiddish',
            description: '',
            comment: ''
        },
        {
            id: '102',
            name: 'Yoruba',
            description: '',
            comment: ''
        },
        {
            id: '103',
            name: 'Zulu',
            description: '',
            comment: ''
        }
    ];
    langList.getLanguages = function () {
        return languages;
    }

    langList.getLanguage = function (index) {
        return languages[index];
    }
    return langList;

};

module.exports = {
    factory: langListFactory
};