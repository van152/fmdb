__int64 __fastcall sub_1409728C0(__int64 a1, unsigned int a2, __int64 a3)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  unsigned __int64 v8; // rbx
  __int64 v9; // rdi
  char v10; // al
  __int64 v11; // rdx
  __int64 v12; // rbp
  __int64 v13; // rsi
  __int64 v15; // rsi

  v4 = *(_QWORD *)(a1 + 448);
  v5 = *(_QWORD *)(a1 + 456);
  if ( v5 == v4 )
    return 0;
  if ( a3 == 0 )
  {
    v15 = 0;
    while ( 1 )
    {
      v9 = *(_QWORD *)(v4 + 8 * v15);
      if ( v9 != 0 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 624LL))(v9) != 0 )
          return (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v9 + 1080LL))(v9, a2, 0);
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 632LL))(v9) != 0 )
          goto LABEL_18;
        v4 = *(_QWORD *)(a1 + 448);
        v5 = *(_QWORD *)(a1 + 456);
      }
      if ( ++v15 >= (unsigned __int64)((v5 - v4) >> 3) )
        return 0;
    }
  }
  v8 = 0;
  while ( 1 )
  {
    v9 = *(_QWORD *)(v4 + 8 * v8);
    if ( v9 != 0 )
    {
      v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 624LL))(v9);
      v11 = *(_QWORD *)v9;
      if ( v10 != 0 )
      {
        if ( (*(__int64 (__fastcall **)(__int64))(v11 + 296))(v9) == 0
          || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 296LL))(v9) == a3 )
        {
          return (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v9 + 1080LL))(v9, a2, 0);
        }
        goto LABEL_4;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(v11 + 632))(v9) != 0 )
      {
        if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 296LL))(v9) == 0
          || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 296LL))(v9) == a3 )
        {
          goto LABEL_18;
        }
        if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 784LL))(v9) != 0 )
          break;
      }
    }
LABEL_4:
    ++v8;
    v4 = *(_QWORD *)(a1 + 448);
    if ( v8 >= (*(_QWORD *)(a1 + 456) - v4) >> 3 )
      return 0;
  }
  v12 = 0;
  while ( 1 )
  {
    v13 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v9 + 792LL))(v9, v12);
    if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v13 + 296LL))(v13) == a3
      && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v13 + 272LL))(v13) == 0 )
    {
      break;
    }
    v12 = (unsigned __int8)(v12 + 1);
    if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 784LL))(v9) <= (unsigned __int64)(unsigned __int8)v12 )
      goto LABEL_4;
  }
LABEL_18:
  if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 784LL))(v9) != 0 )
  {
    v9 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v9 + 808LL))(v9, 0);
    return (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v9 + 1080LL))(v9, a2, 0);
  }
  return 0;
}
