

declare class Mode extends cc.Component {
    // export abstract class Mode extends cc.Component {
    /** 是否展示此模式 */
    public bShow: boolean
    /** 当前mode的名字用于item显示 */
    public abstract modeName: string;
    /** 获取当前的模式下的spine骨骼对象 */
    protected spine: sp.Skeleton;
    /** 
     *  需要被渲染的节点  
     *  在此列表中的节点会计算dc进去
     */
    protected vRenderNode: Array<cc.Node>;
    /** 手动刷新dc */
    public initDC(): void;
    /**
     * 同ccc骨骼动画
     * @param sAniName 
     * @param bLoop = true
     */
    public setAnimation(sAniName: string, bLoop?: boolean): void;
    /** 需要被渲染展示dc的列表 */
    public addRenderDCList(...vNode): void
    // }
}
