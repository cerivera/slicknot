var casper = require('casper').create({
    verbose: true,
    logLevel: 'debug'
});

var deals = [];

casper.start('http://slickdeals.net', function() {
    function _getV1Deals() {
        var fpDeals = document.querySelectorAll('span.dealblocktext');

        return Array.prototype.map.call(fpDeals, function(e) {
            var deal = {};

            var titleLink = e.querySelector('strong a');
            if (titleLink) {
                deal.title = e.textContent;
                deal.link = e.href;
            };

            var priceElm = e.querySelector('strong b');
            if (priceElm) {
                deal.price = e.textContent;
            }

            return deal;
        });
    }

    function _getV2Deals() {
        var fpDeals = document.querySelectorAll('div.fpItem');

        return Array.prototype.map.call(fpDeals, function(e) {
            var deal = {};

            var titleLink = e.querySelector('a.itemTitle');
            if (titleLink) {
                deal.title = titleLink.textContent;
                deal.link = titleLink.href;
            }

            var priceElm = e.querySelector('.priceLine .itemPrice');
            if (priceElm) {
                deal.price = priceElm.textContent;
            }

            return deal;
        });
    }

    var newDeals = this.evaluate(_getV1Deals);
    if (!newDeals.length) {
        casper.log('Trying Slickdeals v2 scraper', 'debug');
        newDeals = this.evaluate(_getV2Deals);
    }

    if (!newDeals.length) {
        casper.log('Could not fetch results from Slickdeals', 'error');
    }

    deals = deals.concat(newDeals);
});

// REI Outlet Cycles
casper.thenOpen('http://www.rei.com/outlet/c/bikes?ir=category%3Abikes&pagesize=90&sort=percentageoff&outlet=true&r=deals%3AOutlet%20Products%7CClearance%20Products%3Bcategory%3Acycling%7Cbikes%3Bgender%3AUnisex%7CWomen%27s%7CMen%27s&page=1&version=v2&rank=test-version-2');

casper.waitFor(function check() {
    return this.evaluate(function() {
        return document.querySelectorAll('.product-details').length > 10;
    });
}, function then() {
    function _getDeals() {
        var _deals = document.querySelectorAll('.product-details');
        return Array.prototype.map(_deals, function(e) {
            var deal = {};

            var linkElm = e.querySelector('.result-product-page-link');
            if (linkElm) {
                deal.link = linkElm.href;
            }

            var titleElm = e.querySelector('.result-product-page-link .result-title');
            if (titleElm) {
                deal.title = titleElm.textContent;
            }

            var priceElm = e.querySelector('.result-product-page-link li.sale-price');
            if (priceElm) {
                deal.price = priceElm.textContent;
            }

            return deal;
        });
    }

    deals = deals.concat(this.evaluate(_getDeals));

});


casper.run(function() {
    this.echo(deals.length + ' deals found:');
    for (var i = 0; i < deals.length; i++) {
        this.echo(deals[i].title + '\n');
    }
    this.exit();
});
