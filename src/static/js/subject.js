export class Subject {
    constructor() {
        this._callbacks = [];
    }

    addListener(event, listener) {
        this._callbacks.push([event, listener]);
    }

    async notify(event, data) {

        const promises = [];

        this._callbacks.forEach((eventCallbackTuple) => {
            const [listenEvent, listener] = eventCallbackTuple;
            if (event === listenEvent) {
                const updatePromise = listener.update(data);
                promises.push(updatePromise);
            }
        });

        return Promise.all(promises);
    }
}