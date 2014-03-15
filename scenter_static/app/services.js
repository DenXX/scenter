var scenterServices = angular.module('scenterServices', ['ngResource']);
 
scenterServices.factory('Fences', ['$resource',
  function($resource){
    return $resource('/api/fences/', {}, {
      query: {method:'GET', params:{bbox:''}, isArray:true}
    });
  }]);

scenterServices.factory('Scents', ['$resource',
  function($resource){
    return $resource('/api/scents/', {}, {
      query: {method:'GET', params:{fence_id:''}, isArray:true}
    });
  }]);

