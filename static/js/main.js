var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var Stop = (function (_super) {
    __extends(Stop, _super);
    function Stop(attributes, options) {
        return _super.call(this, attributes, options) || this;
    }
    Stop.prototype.defaults = function () {
        return {
            id: null,
            wheelchair_boarding: 0,
            start_date: null,
            end_date: null,
            name: new StopNameList(),
            positions: new StopPositionList(),
            url: new StopUrlList()
        };
    };
    Stop.prototype.initialize = function () {
        if (!this.get("name")) {
            this.set({ "name": this.defaults().name });
        }
        if (!this.get("positions")) {
            this.set({ "positions": this.defaults().positions });
        }
        if (!this.get("url")) {
            this.set({ "url": this.defaults().url });
        }
    };
    return Stop;
}(Backbone.Model));
var StopList = (function (_super) {
    __extends(StopList, _super);
    function StopList() {
        var _this = _super.apply(this, arguments) || this;
        _this.model = Stop;
        return _this;
    }
    return StopList;
}(Backbone.Collection));
var StopName = (function (_super) {
    __extends(StopName, _super);
    function StopName(attributes, options) {
        return _super.call(this, attributes, options) || this;
    }
    return StopName;
}(Backbone.Model));
var StopNameList = (function (_super) {
    __extends(StopNameList, _super);
    function StopNameList() {
        var _this = _super.apply(this, arguments) || this;
        _this.model = StopName;
        return _this;
    }
    return StopNameList;
}(Backbone.Collection));
var StopPosition = (function (_super) {
    __extends(StopPosition, _super);
    function StopPosition(attributes, options) {
        return _super.call(this, attributes, options) || this;
    }
    return StopPosition;
}(Backbone.Model));
var StopPositionList = (function (_super) {
    __extends(StopPositionList, _super);
    function StopPositionList() {
        var _this = _super.apply(this, arguments) || this;
        _this.model = StopPosition;
        return _this;
    }
    return StopPositionList;
}(Backbone.Collection));
var StopUrl = (function (_super) {
    __extends(StopUrl, _super);
    function StopUrl(attributes, options) {
        return _super.call(this, attributes, options) || this;
    }
    return StopUrl;
}(Backbone.Model));
var StopUrlList = (function (_super) {
    __extends(StopUrlList, _super);
    function StopUrlList() {
        var _this = _super.apply(this, arguments) || this;
        _this.model = StopUrl;
        return _this;
    }
    return StopUrlList;
}(Backbone.Collection));
