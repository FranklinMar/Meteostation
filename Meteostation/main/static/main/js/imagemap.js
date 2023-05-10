$('img[usemap]').maphilight({fill: true, fillOpacity: 0.25, fillColor: '000000', fade: true, strokeColor: '1F3C5C',
    strokeWidth: 3, shadow: true/*, shadowColor: 'FFFFFF'*/});
$('area').each(function(){
    let title = $(this).attr('title');
    let coords = $(this).attr('coords').split("  ");
    let left = parseInt(coords[0].split(',')[0]), top = parseInt(coords[0].split(',')[1]),
        right = parseInt(coords[0].split(',')[0]), bottom = parseInt(coords[0].split(',')[1]);
    for (let i = 1; i < coords.length; i++) {
        let t_x = parseInt(coords[i].split(',')[0]), t_y = parseInt(coords[i].split(',')[1]);
        if (t_x > right) {
            right = t_x;
        } else if (t_x < left) {
            left = t_x;
        }
        if (t_y > bottom) {
            bottom = t_y;
        } else if (t_y < top) {
            top = t_y
        }
    }
    //let map_top = $('.map').top, map_left = $('.map').left;
    let left_title = left + (right - left) / 2,
        top_title = top + (bottom - top) / 2;
        //right_title = right - (right - left) / 2;
    let span = $(`<span class='map_title'>${title.replace('-', '-<br>-')}</span>`);
    /*if ((right_title - left_title) <= span.width) {
        span = $(`<span class='map_title'>${span.innerText.replace("-", "-<br>-")}</span>`);
    }*/
    let padding = parseInt($('.map').css('padding').split(' ')[1]);
    span.data('title', title);
    span.css({top:(top_title + parseFloat($(this).data('offset-y'))) + 'px', position:'absolute',
        transition:'0.1s linear', pointerEvents:'none'});
    span.appendTo('.map');
    span.css({left:(left_title - Math.ceil(span.width() / 2) + padding + parseFloat($(this).data('offset-x'))) + 'px'});
});
/*$('area').mouseover(function() {
    $('.map span[data-title="' + $(this).attr('title') + '"]').css({color:'#FFFFFF'});
});
$('area').mouseout(function() {
    $('.map span[data-title="' + $(this).attr('title') + '"]').css({color:'#000000'});
});*/