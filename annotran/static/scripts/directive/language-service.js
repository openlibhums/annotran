'use strict';
function langListFactory() {
        var langList = {};
        var languages=[
                        {
                           id: '1',
                           name:'English',
                           description:'',
                           comment: ''
                        },
                        {
                           id: '2',
                           name:'Italian',
                           description:'',
                           comment: ''
                        },
                        {
                           id: '3',
                           name:'French',
                           description:'',
                           comment: ''
                        },
                        {
                           id: '4',
                           name:'Swedish',
                           description:'',
                           comment: ''
                        },
                        {
                           id: '5',
                           name:'Spanish',
                           description:'',
                           comment: ''
                        },
                        {
                           id: '6',
                           name:'Mongolian',
                           description:'',
                           comment: ''
                        }
                        ];
        langList.getLanguages = function() {
            return languages;
        }

        langList.getLanguage = function(index) {
            return languages[index];
        }
        return langList;

};

module.exports = {
  factory: langListFactory
};