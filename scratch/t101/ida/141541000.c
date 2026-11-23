int *__fastcall sub_141541000(int *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // rbx
  __int64 v6; // rdi
  int v7; // eax
  __int64 v8; // r15
  __int64 v9; // rsi
  __int64 v10; // r12
  __int64 v11; // rbp
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // rbp
  __int64 v17; // rdi
  __int64 *v18; // rsi
  __int64 v19; // rbx
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // r15
  unsigned __int64 v22; // r14
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // r14
  __int64 v25; // r12
  __int64 *v26; // rdi
  __int64 v27; // rdi
  unsigned __int64 v28; // rcx
  __int64 v29; // rbx
  __int64 v30; // rsi
  unsigned int v32; // [rsp+24h] [rbp-54h] BYREF
  int *v33; // [rsp+28h] [rbp-50h]
  _QWORD *v34; // [rsp+30h] [rbp-48h]

  v4 = a2;
  v32 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v32, 4);
  v6 = v32;
  v7 = 1;
  if ( qword_141AA7808 <= (unsigned __int64)v32 )
    goto LABEL_44;
  v33 = a1;
  v8 = *a3;
  if ( (a3[2] - *a3) >> 3 >= (unsigned __int64)v32 )
    goto LABEL_14;
  v9 = a3[1];
  v10 = sub_1407E4490(qword_141ABD470, 8LL * v32);
  sub_141758A00(v10, *a3, a3[1] - *a3);
  v11 = *a3;
  if ( *a3 != 0 )
  {
    v12 = a3[2] - v11;
    if ( v12 == -1 )
    {
      v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](v11 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12 )
    {
      v14 = *(_QWORD *)(v13 + 8 * v12);
      if ( v14 != 0 )
      {
        MEMORY[0x1419475D8](v14 + 32, v11 - *(unsigned int *)(v14 + 120));
        v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
        if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
          sub_1412D33C0(v14);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_13:
  *a3 = v10;
  a3[1] = v10 + v9 - v8;
  a3[2] = v10 + 8 * v6;
  LODWORD(v6) = v32;
LABEL_14:
  if ( (_DWORD)v6 == 0 )
    goto LABEL_43;
  v16 = 0;
  v34 = v4;
  while ( 1 )
  {
    v17 = sub_141541370(24);
    *(_QWORD *)v17 = 0;
    *(_QWORD *)(v17 + 8) = 0;
    *(_WORD *)(v17 + 16) = 1900;
    *(_DWORD *)(v17 + 18) = -10223361;
    if ( (unsigned __int8)sub_1414A8D40(v17, v4) == 0 )
    {
      sub_141540F00(v17);
      a1 = v33;
      v7 = 1;
      goto LABEL_44;
    }
    if ( *(_DWORD *)(*v4 + 16LL) != 0 )
      break;
    v18 = (__int64 *)a3[1];
    if ( v18 == (__int64 *)a3[2] )
    {
      v19 = (__int64)v18 - *a3;
      v20 = v19 >> 3;
      v21 = (v19 >> 3) + 1;
      v22 = (unsigned __int64)(v19 >> 3) >> 1;
      v23 = 0x1FFFFFFFFFFFFFFFLL - v22;
      v24 = (v19 >> 3) + v22;
      if ( v24 <= v21 )
        v24 = v20 + 1;
      if ( v20 > v23 )
        v24 = 0x1FFFFFFFFFFFFFFFLL;
      v25 = sub_1407E4490(qword_141ABD470, 8 * v24);
      *(_QWORD *)(v25 + v19) = v17;
      v26 = (__int64 *)a3[1];
      sub_141758A00(v25, *a3, (char *)v18 - *a3);
      if ( v26 != v18 )
        sub_141758A00(v25 + v19 + 8, v18, a3[1] - (_QWORD)v18);
      v27 = *a3;
      if ( *a3 != 0 )
      {
        v28 = a3[2] - v27;
        if ( v28 == -1 )
        {
          v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_37;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_37;
        }
        v29 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28 && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
        {
          MEMORY[0x1419475D8](v30 + 32, v27 - *(unsigned int *)(v30 + 120));
          if ( (*(_BYTE *)(v30 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) == 0)
            && *(_BYTE *)(v30 + 97) != 0 )
          {
            sub_1412D33C0(v30);
          }
        }
        else
        {
LABEL_37:
          MEMORY[0x141948990](v27 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *a3 = v25;
      a3[1] = v25 + 8 * v21;
      a3[2] = v25 + 8 * v24;
      v4 = v34;
      goto LABEL_17;
    }
    *v18 = v17;
    a3[1] += 8;
LABEL_17:
    if ( ++v16 >= (unsigned __int64)v32 )
      goto LABEL_43;
  }
  sub_141540F00(v17);
LABEL_43:
  v7 = *(_DWORD *)(*v4 + 16LL);
  a1 = v33;
LABEL_44:
  *a1 = v7;
  return a1;
}
