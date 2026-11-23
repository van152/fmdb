__int64 __fastcall sub_1409725C0(__int64 a1, unsigned int a2, unsigned int a3)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 v8; // rbp
  __int64 v9; // rsi

  v4 = *(_QWORD *)(a1 + 448);
  v5 = *(_QWORD *)(a1 + 456);
  if ( v5 == v4 )
    return 0;
  v8 = 0;
  while ( 1 )
  {
    v9 = *(_QWORD *)(v4 + 8 * v8);
    if ( v9 != 0 )
      break;
LABEL_3:
    if ( ++v8 >= (unsigned __int64)((v5 - v4) >> 3) )
      return 0;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 624LL))(v9) != 0 )
    return (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v9 + 1072LL))(v9, a2, a3);
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 632LL))(v9) == 0 )
  {
    v4 = *(_QWORD *)(a1 + 448);
    v5 = *(_QWORD *)(a1 + 456);
    goto LABEL_3;
  }
  if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 784LL))(v9) == 0 )
    return 0;
  v9 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v9 + 808LL))(v9, 0);
  return (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v9 + 1072LL))(v9, a2, a3);
}
