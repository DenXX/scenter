var scenterServices = angular.module('scenterServices', ['ngResource']);
 
scenterServices.factory('Scent', ['$resource',
  function($resource){
    return $resource('phones/:phoneId.json', {}, {
      query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
    });
  }]);