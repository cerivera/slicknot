var casper = require('casper').create({
    verbose: true,
    logLevel: 'debug'
});

function getParsedPrice(val) {
    if (val == undefined || val == null) {
        return 'N/A';
    }

    var parsedVal = yankFloatFromStr(val);
    return parsedVal == null ? val : parsedVal;
}

function yankFloatFromStr(val) {
    var strippedVal = val.replace(/[^\d\.]/g, '');
    if (strippedVal) {
        try {
            return parseFloat(strippedVal);
        } catch(err) {
            return null;
        }
    }
    return null;
}

var deals = [];

casper.start('http://slickdeals.net', function() {
    function _getV1Deals() {
        var fpDeals = document.querySelectorAll('span.dealblocktext');

        return Array.prototype.map.call(fpDeals, function(e) {
            var deal = {};

            var titleLink = e.querySelector('strong a');
            if (titleLink) {
                deal.title = titleLink.textContent;
                deal.link = titleLink.href;
            };

            var priceElm = e.querySelector('strong b');
            if (priceElm) {
                deal.price = priceElm.textContent;
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

casper.run(function() {
    this.echo(deals.length + ' deals found:');
    for (var i = 0; i < deals.length; i++) {
        this.echo(deals[i].title + " : " + getParsedPrice(deals[i].price) + '\n');
    }
    this.exit();
});
