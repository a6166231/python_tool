
export class testMode extends Mode {
    public modeName: string = '测试哦';

    onLoad() {
        super.onLoad();
        this.spine.node.on(cc.Node.EventType.TOUCH_END, this.test123, this)
    }

    test123() {
        // cc.find
        console.log(1);
    }
}
