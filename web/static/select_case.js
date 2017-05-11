/**
 * Created by Administrator on 2016/8/25.
 */

//父节点选中/不选中，全选/不全选子节点
function allSelect(check_v, checkname)
{
    var v_item = document.getElementsByName(check_v);
    var items = document.getElementsByClassName(checkname);
    for (var i = 0; i < items.length; ++i)
    {
        if (v_item[0].checked)
        {
            items[i].checked = true;
        }
        else
        {
            items[i].checked = false;
        }
    }
}

//子节点选中，检查父节点状态
function singleSelect2parent(check_v, checkname)
{
    var v_item = document.getElementsByName(check_v);
    var items = document.getElementsByClassName(checkname);
    var childStatus = true;
    for (var i = 0; i < items.length; ++i)
    {
        childStatus = (childStatus && items[i].checked);
    }
    if (childStatus)
    {
        v_item[0].checked = true;
    }
    else
    {
        v_item[0].checked = false;
    }
}
