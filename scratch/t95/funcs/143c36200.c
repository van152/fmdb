__int64 __fastcall sub_143C36200(_QWORD *a1, char a2, char a3, char a4)
{
  __int64 v8; // rdx
  __int64 v9; // r9
  char *v10; // rax
  char *v11; // rdi
  unsigned __int64 v12; // rcx
  unsigned __int64 v13; // rcx
  __int64 v14; // rbx
  __int64 v15; // rcx
  __int64 v17; // r8
  unsigned __int64 v18; // rbp
  __int64 v19; // rax
  __int64 v20; // rax
  __int64 v21; // rdi
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // rdx

  if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*a1 + 352LL))(a1) != 0 )
    goto LABEL_21;
  if ( (unsigned __int8)(a2 - 3) >= 2u )
  {
    v10 = (char *)a1[3];
    v11 = (char *)a1[4];
LABEL_11:
    if ( v10 == v11 )
      LODWORD(v17) = 0;
    else
      v17 = *(_QWORD *)v10;
    goto LABEL_14;
  }
  v10 = (char *)a1[3];
  v11 = (char *)a1[4];
  v12 = (unsigned __int64)(v11 - v10) >> 3;
  if ( (int)v12 <= 0 )
    goto LABEL_11;
  v13 = v12 + 0xFFFFFFFF;
  v14 = (unsigned int)v13 + 1LL;
  v15 = v13 << 56;
  v9 = 0x220263E00LL;
  while ( 1 )
  {
    v8 = v15 >> 53;
    v17 = *(_QWORD *)&v10[v15 >> 53];
    if ( v17 != 0 )
    {
      v18 = (unsigned int)*(char *)(v17 + 40);
      if ( (unsigned int)v18 <= 0x21 )
      {
        if ( _bittest64(&v9, v18) )
          break;
      }
    }
    v15 -= 0x100000000000000LL;
    if ( v14-- <= 1 )
      goto LABEL_11;
  }
LABEL_14:
  LOBYTE(v8) = -106;
  LOBYTE(v9) = 1;
  v19 = sub_1411D9CF0((_DWORD)a1, v8, v17, v9, 1);
  if ( v19 != 0 )
  {
    v20 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v19 + 1688LL))(v19);
    if ( v20 != 0 )
    {
      v21 = v20;
      if ( a3 == 0 )
        return v21;
      v22 = v20 + *(int *)(*(_QWORD *)(v20 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v22 + 528LL))(v22) == 0 )
        return v21;
      if ( a1[3] == a1[4] )
      {
        v21 = 0;
      }
      else
      {
        v21 = 0;
        v23 = sub_1411DC000((_DWORD)a1, 0, 0, 0, 1, 0);
        if ( v23 != 0 )
        {
          LOBYTE(v24) = 4;
          v21 = sub_1411A43E0(v23, v24);
        }
      }
      if ( v21 != 0 || a4 == 0 )
        return v21;
      return sub_1411D7430(a1);
    }
  }
LABEL_21:
  if ( a4 != 0 )
    return sub_1411D7430(a1);
  return 0;
}
