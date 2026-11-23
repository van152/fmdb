int *__fastcall sub_141541480(int *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // r13
  __int64 v6; // rdi
  int v7; // eax
  __int64 v8; // r15
  __int64 v9; // rbp
  __int64 v10; // r12
  __int64 v11; // rsi
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // r15
  _QWORD *v17; // r14
  _QWORD *v18; // r12
  __int64 v19; // r13
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // rsi
  unsigned __int64 v22; // rcx
  unsigned __int64 v23; // rsi
  __int64 v24; // rbp
  _QWORD *v25; // rdi
  __int64 v26; // rdi
  unsigned __int64 v27; // rcx
  __int64 v28; // r8
  __int64 v29; // r14
  unsigned int v31; // [rsp+4Ch] [rbp-5Ch] BYREF
  int *v32; // [rsp+50h] [rbp-58h]
  _QWORD *v33; // [rsp+58h] [rbp-50h]
  unsigned __int64 v34; // [rsp+60h] [rbp-48h]

  v4 = a2;
  v31 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v31, 4);
  v6 = v31;
  v7 = 1;
  if ( qword_141AA7808 <= (unsigned __int64)v31 )
    goto LABEL_47;
  v32 = a1;
  v8 = *a3;
  if ( (a3[2] - *a3) >> 3 >= (unsigned __int64)v31 )
    goto LABEL_14;
  v9 = a3[1];
  v10 = sub_1407E4490(qword_141ABD470, 8LL * v31);
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
  LODWORD(v6) = v31;
LABEL_14:
  if ( (_DWORD)v6 == 0 )
    goto LABEL_46;
  v16 = 0;
  v33 = v4;
  while ( 1 )
  {
    if ( dword_141B63F50 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B63F50);
      if ( dword_141B63F50 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141B63F00, 1100136831, 16, 24, 0, 0, 16, 4096);
        sub_141751048(sub_1414478B0);
        sub_141750EA0(&dword_141B63F50);
      }
    }
    v17 = (_QWORD *)sub_1407E58C0(&unk_141B63F00, 24);
    v17[2] = 124518401;
    *v17 = 0x1418B6998LL;
    v17[1] = 0;
    if ( (unsigned __int8)sub_1414D3620(v17, v4) == 0 )
    {
      sub_141447740(v17);
      a1 = v32;
      v7 = 1;
      goto LABEL_47;
    }
    if ( *(_DWORD *)(*v4 + 16LL) != 0 )
      break;
    v18 = (_QWORD *)a3[1];
    if ( v18 == (_QWORD *)a3[2] )
    {
      v19 = (__int64)v18 - *a3;
      v20 = v19 >> 3;
      v21 = (unsigned __int64)(v19 >> 3) >> 1;
      v22 = 0x1FFFFFFFFFFFFFFFLL - v21;
      v23 = (v19 >> 3) + v21;
      v34 = (v19 >> 3) + 1;
      if ( v23 <= v34 )
        v23 = v20 + 1;
      if ( v20 > v22 )
        v23 = 0x1FFFFFFFFFFFFFFFLL;
      v24 = sub_1407E4490(qword_141ABD470, 8 * v23);
      *(_QWORD *)(v24 + v19) = v17;
      v25 = (_QWORD *)a3[1];
      sub_141758A00(v24, *a3, (char *)v18 - *a3);
      if ( v25 != v18 )
        sub_141758A00(v24 + v19 + 8, v18, a3[1] - (_QWORD)v18);
      v26 = *a3;
      v4 = v33;
      if ( *a3 != 0 )
      {
        v27 = a3[2] - v26;
        if ( v27 == -1 )
        {
          v27 = *(unsigned int *)(v26 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_38;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_38;
        }
        v28 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v28) >> 3 > v27 && (v29 = *(_QWORD *)(v28 + 8 * v27)) != 0 )
        {
          MEMORY[0x1419475D8](v29 + 32, v26 - *(unsigned int *)(v29 + 120));
          if ( (*(_BYTE *)(v29 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) == 0)
            && *(_BYTE *)(v29 + 97) != 0 )
          {
            sub_1412D33C0(v29);
          }
        }
        else
        {
LABEL_38:
          MEMORY[0x141948990](v26 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *a3 = v24;
      a3[1] = v24 + 8 * v34;
      a3[2] = v24 + 8 * v23;
      goto LABEL_17;
    }
    *v18 = v17;
    a3[1] += 8;
LABEL_17:
    if ( ++v16 >= (unsigned __int64)v31 )
      goto LABEL_46;
  }
  sub_141447740(v17);
LABEL_46:
  v7 = *(_DWORD *)(*v4 + 16LL);
  a1 = v32;
LABEL_47:
  *a1 = v7;
  return a1;
}
