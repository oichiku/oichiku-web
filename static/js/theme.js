const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
const darkModeOn = darkModeMediaQuery.matches;

$(document).ready(function(){
    if (darkModeOn) { // Dark
        $('.twitter').html('<a class="twitter-timeline" href="https://twitter.com/oichiku_?ref_src=twsrc%5Etfw" data-tweet-limit="1" data-chrome="transparent" data-theme="dark">Tweets by @oichiku_<\/a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><\/script>')
    } else { // Light
        $('.twitter').html('<a class="twitter-timeline" href="https://twitter.com/oichiku_?ref_src=twsrc%5Etfw" data-tweet-limit="1" data-chrome="transparent" data-theme="light">Tweets by @oichiku_<\/a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><\/script>')
    }
});

darkModeMediaQuery.addListener((e) => {
    const darkModeOn = e.matches;
    if (darkModeOn) { // Dark
        $('.twitter').html('<a class="twitter-timeline" href="https://twitter.com/oichiku_?ref_src=twsrc%5Etfw" data-tweet-limit="1" data-chrome="transparent" data-theme="dark">Tweets by @oichiku_<\/a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><\/script>')
    } else { // Light
        $('.twitter').html('<a class="twitter-timeline" href="https://twitter.com/oichiku_?ref_src=twsrc%5Etfw" data-tweet-limit="1" data-chrome="transparent" data-theme="light">Tweets by @oichiku_<\/a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><\/script>')
    }
});