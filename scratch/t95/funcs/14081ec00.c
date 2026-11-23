// THUNK ALIAS -> sub_143730470 (jmp:0x14081ec00->0x143730470)
_QWORD *__fastcall sub_143730470(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rsi
  __int64 v6; // rcx
  __int64 v7; // rax
  __int64 *v8; // rdi
  __int64 v9; // rax
  __int64 v10; // rdx
  __int64 v11; // rcx
  __int64 v13; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v14[6]; // [rsp+30h] [rbp-10h] BYREF

  v14[1] = -2;
  v4 = qword_141ABD468;
  v14[0] = 0;
  if ( *(_DWORD *)(a1 + 24) == -1
    || (v5 = *(_QWORD *)(*(_QWORD *)(qword_141ABD468 + 8) + 64LL), *(_QWORD *)(sub_140105F10() + 16) != v5) )
  {
    sub_14081DFC0(a1, 0, 0xFFFFFFFFLL, &qword_141B59EE0);
    if ( *(_DWORD *)(*(_QWORD *)(v4 + 8) + 264LL) != 0 )
    {
      sub_14081EDF0(a1, &v13);
      v7 = v13;
      if ( v13 == 0 )
        goto LABEL_10;
    }
    else
    {
      v8 = (__int64 *)(a1 + 8);
      if ( v8 == v14 )
        goto LABEL_10;
      v7 = *v8;
      if ( *v8 != 0 )
      {
        v14[0] = 0;
        _InterlockedIncrement((volatile signed __int32 *)(v7 - 4));
      }
    }
    v14[0] = v7;
  }
LABEL_10:
  v9 = sub_14083D4F0(v6);
  a2[1] = 0;
  if ( a2 + 1 != v14 )
  {
    v10 = v14[0];
    if ( v14[0] != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v14[0] - 4LL));
    a2[1] = v10;
  }
  *a2 = v9 + 136;
  v11 = v14[0];
  if ( v14[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14[0] - 4LL)) == 0 )
    sub_1412EC9A0(v11 - 4);
  return a2;
}
