$('.produtodatalist').flexdatalist({
 minLength: 1,
 searchIn: ['descricao', 'codigo'],
 searchContain: true,
 //searchDisabled: true,
 url: 'http://localhost/listar_produtos/json/',
 keywordParamName: 'search',
 requestType: 'get',
 //requestHeaders: {credentials: 'include'},
 visibleProperties: ['descricao', 'codigo'],
 searchByWord: true,
 noResultsText: 'Sem resultados para: "{keyword}"',
 valueProperty: 'id',
 textProperty: '{descricao} - {codigo}'
});

$('input.produtodatalist').on('select:flexdatalist', function(event, item, options){

    //document.getElementById("search-form").submit();
    redirect = window.location.protocol + "//" + window.location.hostname + "/listar_estoque/" + item.id
    window.location.href = redirect;
})
