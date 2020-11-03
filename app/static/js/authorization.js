function getAjaxInformation(url) {
    let response = null;
    $.ajax({
        type: "GET",
        url: url,
        async: false,
        success: function (text) {
            response = text;
        }
    });
    return response;
}

$('.logo img').click(function () {
    let response = getAjaxInformation('api/authorize/github');
    window.location.href = response;
});