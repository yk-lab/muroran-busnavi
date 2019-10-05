import {Model, Collection} from "backbone";

export class Stop extends Model {
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

export class StopName extends Model {
  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }
}

export class StopList extends Collection<Stop> {
  model = Stop;
}

export class StopNameList extends Collection<StopName> {
  model = StopName;
}

export class StopPosition extends Model {
  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }
}

export class StopPositionList extends Collection<StopPosition> {
  model = StopPosition;
}

export class StopUrl extends Model {
  constructor(attributes?: any, options?: any) {
    super(attributes, options);
  }
}

export class StopUrlList extends Collection<StopUrl> {
  model = StopUrl;
}
