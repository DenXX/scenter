
var scenterControllers = angular.module('scenterControllers', []);
 
scenterControllers.controller('ScentListCtrl', ['$scope', '$http', function ($scope) {
  $scope.scents = [
    {'content': 'This is sample scent text. This is sample scent text. This is sample scent text. This is sample scent text. ',
     'fence': 'Emory University',
     'author': "DenXX"},
    {'content': 'I don\'t understand what you are saying. I don\'t understand what you are saying. I don\'t understand what you are saying. ',
     'fence': 'China',
     'author': "YuWang"},
    {'content': 'This is sample scent text. This is sample scent text. This is sample scent text. This is sample scent text. ',
     'fence': 'Emerson Hall',
     'author': "DavidFink"}
  ];
}]);