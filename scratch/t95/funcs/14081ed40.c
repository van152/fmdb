// THUNK ALIAS -> sub_1437306D0 (jmp:0x14081ed40->0x1437306d0)
__int64 *__fastcall sub_1437306D0(__int64 a1, __int64 *a2, unsigned int a3)
{
  __int64 v6; // rbx
  __int64 v7; // rbp
  __int64 v8; // rax
  __int64 *v9; // rdi
  _QWORD v11[6]; // [rsp+28h] [rbp-30h] BYREF

  v6 = qword_141ABD468;
  *a2 = 0;
  if ( *(_DWORD *)(a1 + 24) == -1
    || (v7 = *(_QWORD *)(*(_QWORD *)(v6 + 8) + 64LL), *(_QWORD *)(sub_140105F10() + 16) != v7) )
  {
    sub_14081DFC0(a1, a3, 0xFFFFFFFFLL, &qword_141B59EE0);
    if ( *(_DWORD *)(*(_QWORD *)(v6 + 8) + 264LL) != 0 )
    {
      sub_14081EDF0(a1, v11);
      v8 = v11[0];
      if ( v11[0] == 0 )
        return a2;
      goto LABEL_10;
    }
    v9 = (__int64 *)(a1 + 8);
    if ( v9 != a2 )
    {
      v8 = *v9;
      if ( *v9 != 0 )
      {
        *a2 = 0;
        _InterlockedIncrement((volatile signed __int32 *)(v8 - 4));
      }
      else
      {
        v8 = 0;
      }
LABEL_10:
      *a2 = v8;
    }
  }
  return a2;
}
