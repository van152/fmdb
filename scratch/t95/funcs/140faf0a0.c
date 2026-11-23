// THUNK ALIAS -> sub_143DCC730 (jmp:0x140faf0a0->0x143dcc730)
__int64 __fastcall sub_143DCC730(__int64 a1, int a2)
{
  _QWORD *v2; // rbx
  __int64 v3; // rdi
  __int64 v4; // rcx
  __int64 v5; // rcx
  __int64 v6; // rcx
  __int64 v7; // rcx
  __int64 result; // rax

  v2 = *(_QWORD **)(a1 + 128);
  v3 = *(_QWORD *)(*v2 + 8LL * a2);
  if ( v3 != 0 )
  {
    sub_140E44A40((__int64 ****)(v3 + 56));
    v4 = *(_QWORD *)(v3 + 48);
    if ( v4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v4 - 4)) == 0 )
      sub_1412EC9A0(v4 - 4);
    v5 = *(_QWORD *)(v3 + 40);
    if ( v5 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v5 - 4)) == 0 )
      sub_1412EC9A0(v5 - 4);
    v6 = *(_QWORD *)(v3 + 32);
    if ( v6 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6 - 4)) == 0 )
      sub_1412EC9A0(v6 - 4);
    v7 = *(_QWORD *)(v3 + 24);
    if ( v7 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v7 - 4)) == 0 )
      sub_1412EC9A0(v7 - 4);
    sub_140FAEF30(v3);
  }
  result = sub_141758A00();
  v2[1] -= 8LL;
  return result;
}
