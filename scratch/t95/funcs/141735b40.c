// THUNK ALIAS -> sub_144765AE0 (jmp:0x141735b40->0x144765ae0)
__int64 __fastcall sub_144765AE0(__int64 a1, __int64 *a2)
{
  __int64 v3; // rsi
  __int64 v4; // rax
  __int64 v5; // rsi
  _QWORD v7[5]; // [rsp+20h] [rbp-28h] BYREF

  v3 = qword_141B5FDD0;
  sub_140FE7960((__int64)v7, a2, 0);
  v4 = sub_14002F670(v3, (int *)v7);
  if ( v4 == 0 )
    return 0;
  v5 = v4;
  if ( sub_141048140(v4, *(_DWORD *)(*(_QWORD *)a1 + 12LL), -1, -1) != nullptr )
    return 0;
  v7[0] = *(_QWORD *)a1;
  v7[1] = 0x76C0001076C0001LL;
  sub_14104DD70(v5, v7);
  return v5;
}
