const Dashboard = require('./views/dashboard');
const Settings = require('./views/settings');

var currentView = null;

var dashboard = new Dashboard();
var settings = new Settings();

const views = {
    dashboard: dashboard,
    settings: settings
}

module.exports = {
    changeView: function(view, io) {
        if (views.hasOwnProperty(view)) {
            views[view].set(true, io)
            if (currentView !== null) currentView.set(false, io)
            currentView = views[view]
        }
    }
}