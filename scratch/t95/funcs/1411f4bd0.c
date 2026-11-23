__int64 __fastcall sub_1411F4BD0(__int64 a1, __int16 a2, unsigned int a3, __int64 a4)
{
  __int64 v4; // r11
  __int64 v5; // r10
  __int64 v6; // rax
  __int64 v7; // rcx
  __int16 v8; // si
  int v9; // edi
  __int64 v10; // rcx

  v4 = *(_QWORD *)(a1 + 24);
  v5 = *(_QWORD *)(a1 + 32) - v4;
  if ( v5 == 0 )
    return 0;
  v6 = 1;
  if ( (unsigned __int64)(v5 >> 3) >= 2 )
    v6 = v5 >> 3;
  v7 = 0;
  v8 = 0;
  while ( 1 )
  {
    v9 = *(unsigned __int8 *)(*(_QWORD *)(v4 + 8 * v7) + 40LL);
    if ( v9 != 22 && v9 != 44 )
    {
      if ( v8 == a2 )
        break;
      ++v8;
    }
    if ( v6 == ++v7 )
      return 0;
  }
  if ( (v7 & 0x8000u) == 0LL && (int)(((unsigned __int64)v5 >> 3) - 1) >= (__int16)v7 )
  {
    v10 = *(_QWORD *)(v4 + 8LL * (unsigned __int16)v7);
    if ( v10 != 0 )
      return (*(__int64 (__fastcall **)(__int64, _QWORD, __int64))(*(_QWORD *)v10 + 16LL))(v10, a3, a4);
  }
  return 0;
}
