char __fastcall sub_143C7B3E0(_QWORD *a1, __int64 **a2)
{
  char v4; // al
  __int64 *v5; // rcx
  __int64 v6; // rbx
  __int64 v7; // rax
  char result; // al
  __int64 v9; // rdx
  _QWORD *v10; // r14
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v14; // rax
  unsigned __int64 v15; // rax
  __int64 v16; // rbx
  __int64 i; // rdi
  __int64 *v18; // rdx
  __int64 v19; // rcx

  v4 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(*a2);
  v5 = *a2;
  v6 = **a2;
  if ( v4 == 10 )
  {
    v7 = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v6 + 176))(v5, a2, 0);
    return sub_140EB2400(a1, v7);
  }
  else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v6 + 8))(v5, a2) == 11 )
  {
    v10 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
    v11 = *(_QWORD *)(a1[1] + 8LL) - *(_QWORD *)a1[1];
    if ( v11 != 0 )
    {
      v12 = (v11 >> 3) - 1;
      do
      {
        v9 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v12);
        if ( v9 != 0 )
          sub_141535A20(*a1, v9, v12);
      }
      while ( v12-- != 0 );
    }
    v14 = v10[1] - *v10;
    if ( v14 != 0 )
    {
      v15 = v14 >> 3;
      v16 = 1;
      if ( v15 >= 2 )
        v16 = v15;
      for ( i = 0; i != v16; ++i )
      {
        v18 = *(__int64 **)(*v10 + 8 * i);
        if ( v18 == nullptr )
          v18 = &qword_141B5A4A0;
        sub_141535920(*a1, v18);
      }
    }
    v19 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_21;
    while ( *(_DWORD *)v19 != 1986359923 )
    {
      v19 += 16;
      if ( v19 == qword_141B60C38 )
        goto LABEL_21;
    }
    if ( v19 == qword_141B60C38 || (result = 1, *(_QWORD *)(v19 + 8) == 0) )
    {
LABEL_21:
      LOBYTE(v9) = 1;
      return sub_140DF8180(a1, v9);
    }
  }
  else
  {
    return 0;
  }
  return result;
}
