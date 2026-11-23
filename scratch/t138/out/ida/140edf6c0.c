char __fastcall sub_140EDF6C0(_BYTE *a1, _QWORD *a2)
{
  __int64 v4; // r8
  __int64 v5; // r8
  _QWORD *v6; // r14
  _QWORD *v7; // rbx
  unsigned int v8; // eax
  __int64 v9; // rcx
  __int64 v10; // r8
  __int64 v11; // r8
  bool v12; // zf
  __int64 v13; // r8
  __int64 v14; // r8
  __int64 v15; // r8
  __int64 v16; // r8
  __int64 v17; // r8
  __int64 v18; // r8
  unsigned __int64 i; // rdi
  __int64 v20; // r8
  __int64 v21; // r8
  char v23; // [rsp+2Ah] [rbp-3Eh] BYREF
  unsigned __int8 v24; // [rsp+2Bh] [rbp-3Dh] BYREF
  unsigned int v25; // [rsp+2Ch] [rbp-3Ch] BYREF
  _BYTE v26[56]; // [rsp+30h] [rbp-38h] BYREF

  v4 = a2[2];
  if ( (unsigned __int8 *)a2[3] == &v24 )
  {
    a2[2] = v4 + 1;
    a2[3] = &v25;
    v25 = 0;
    v6 = a2 + 2;
    v12 = v4 == -5;
    v5 = v4 + 5;
    a2[2] = v5;
    a2[3] = v26;
    if ( v12 )
      goto LABEL_9;
  }
  else
  {
    if ( v4 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1]);
    a2[1] = &v24;
    a2[2] = 1;
    a2[3] = &v25;
    v25 = 0;
    a2[2] = 5;
    v5 = 5;
    a2[3] = v26;
    v6 = a2 + 2;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v5);
LABEL_9:
  v7 = a2 + 1;
  a2[3] = 0;
  a2[2] = 0;
  a2[1] = 0;
  v8 = v25;
  if ( v25 != 0 )
  {
    a2[1] = &v23;
    a2[2] = 1;
    a2[3] = &v24;
    v9 = *a2;
    if ( *a2 != 0 )
    {
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: &v23, a3: 1);
      LOBYTE(v9) = v23;
      v8 = v25;
    }
    a2[3] = 0;
    a2[2] = 0;
    *v7 = 0;
    *a1 = v9;
    if ( v8 >= 2 )
    {
      v10 = a2[2];
      if ( (char *)a2[3] == &v23 )
      {
        v11 = v10 + 1;
        a2[2] = v11;
        a2[3] = &v24;
        if ( v11 == 0 )
          goto LABEL_23;
      }
      else
      {
        if ( v10 != 0 && *a2 != 0 )
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7);
        a2[1] = &v23;
        a2[2] = 1;
        a2[3] = &v24;
        v11 = 1;
      }
      if ( *a2 != 0 )
        (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7, a3: v11);
LABEL_23:
      a2[3] = 0;
      a2[2] = 0;
      *v7 = 0;
      a1[1] = v23;
      if ( v25 < 3 )
        goto LABEL_58;
      v13 = a2[2];
      if ( (char *)a2[3] == &v23 )
      {
        v14 = v13 + 1;
        a2[2] = v14;
        a2[3] = &v24;
        if ( v14 == 0 )
          goto LABEL_32;
      }
      else
      {
        if ( v13 != 0 && *a2 != 0 )
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7);
        a2[1] = &v23;
        a2[2] = 1;
        a2[3] = &v24;
        v14 = 1;
      }
      if ( *a2 != 0 )
        (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7, a3: v14);
LABEL_32:
      a2[3] = 0;
      a2[2] = 0;
      *v7 = 0;
      a1[2] = v23;
      if ( v25 < 4 )
        goto LABEL_58;
      v15 = a2[2];
      if ( (char *)a2[3] == &v23 )
      {
        v16 = v15 + 1;
        a2[2] = v16;
        a2[3] = &v24;
        if ( v16 == 0 )
          goto LABEL_41;
      }
      else
      {
        if ( v15 != 0 && *a2 != 0 )
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7);
        a2[1] = &v23;
        a2[2] = 1;
        a2[3] = &v24;
        v16 = 1;
      }
      if ( *a2 != 0 )
        (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7, a3: v16);
LABEL_41:
      a2[3] = 0;
      a2[2] = 0;
      *v7 = 0;
      a1[3] = v23;
      if ( v25 < 5 )
        goto LABEL_58;
      v17 = a2[2];
      if ( (char *)a2[3] == &v23 )
      {
        v18 = v17 + 1;
        a2[2] = v18;
        a2[3] = &v24;
        if ( v18 == 0 )
        {
LABEL_50:
          a2[3] = 0;
          a2[2] = 0;
          *v7 = 0;
          if ( v25 >= 6 )
          {
            for ( i = 5; i < v25; ++i )
            {
              if ( *v6 != 0 && *a2 != 0 )
                (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7);
              a2[1] = &v23;
              a2[2] = 1;
              a2[3] = &v24;
              if ( *a2 != 0 )
                (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7, a3: 1);
              a2[3] = 0;
              a2[2] = 0;
              *v7 = 0;
            }
          }
          goto LABEL_58;
        }
      }
      else
      {
        if ( v17 != 0 && *a2 != 0 )
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7);
        a2[1] = &v23;
        a2[2] = 1;
        a2[3] = &v24;
        v18 = 1;
      }
      if ( *a2 != 0 )
        (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7, a3: v18);
      goto LABEL_50;
    }
  }
LABEL_58:
  v20 = a2[2];
  if ( (_BYTE *)a2[3] == a1 + 4 )
  {
    *v6 = v20 + 2;
    v21 = v20 + 4;
  }
  else
  {
    if ( v20 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v7);
    a2[1] = a1 + 4;
    a2[2] = 2;
    v21 = 4;
  }
  a2[3] = a1 + 6;
  if ( v24 > 2u )
  {
    a2[2] = v21;
    a2[3] = a1 + 8;
  }
  return 1;
}
