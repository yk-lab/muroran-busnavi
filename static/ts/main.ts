
interface IStop {
    id: string;
    wheelchair_boarding: number;
    start_date: string;
    end_date: string;
    name: any;
    positions: any;
    url: any;
}

interface IStopName {
    id: string;
    stop_code: string;
    name: string;
    desc: string;
    start_date: string;
    end_date: string;
}

interface IStopPosition {
    id: string;
    stop_code: string;
    subname: string;
    desc: string;
    lat: number;
    lng: number;
    geohash: string;
    quadkey: string;
    start_date: string;
    end_date: string;
}

interface IStopUrl {
    id: string;
    stop_code: string;
    url: string;
    start_date: string;
    end_date: string;
}

class Stop extends Backbone.Model {
  defaults() {
    return {
      id: null,
      wheelchair_boarding: 0,
      start_date: null,
      end_date: null,
      name: new StopNameList(),
      positions: new StopPositionList(),
      url: new StopUrlList()
    }
  }

  initialize() {
    if (!this.get("name")) {
      this.set({ "name": this.defaults().name });
    }
    if (!this.get("positions")) {
      this.set({ "positions": this.defaults().positions });
    }
    if (!this.get("url")) {
      this.set({ "url": this.defaults().url });
    }
  }

  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }

}

class StopList extends Backbone.Collection<Stop> {
  model = Stop;
}

class StopName extends Backbone.Model {
  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }
}

class StopNameList extends Backbone.Collection<StopName> {
  model = StopName;
}

class StopPosition extends Backbone.Model {
  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }
}

class StopPositionList extends Backbone.Collection<StopPosition> {
  model = StopPosition;
}

class StopUrl extends Backbone.Model {
  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }
}

class StopUrlList extends Backbone.Collection<StopUrl> {
  model = StopUrl;
}
