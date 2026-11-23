__int64 *__fastcall sub_1444C34E0(__int64 *a1, __int64 a2)
{
  __int64 v2; // rbx
  __int64 **v4; // rax
  __int64 *v5; // rsi
  __int64 *v6; // rcx
  __int64 v7; // r13
  __int64 v8; // rax
  __int64 v9; // rax
  _QWORD *v10; // rdi
  __int64 v11; // r15
  unsigned __int64 v12; // rax
  unsigned __int64 v13; // r14
  unsigned __int64 v14; // rcx
  unsigned __int64 v15; // r14
  __int64 v16; // rbx
  _QWORD *v17; // r13
  __int64 v18; // rdi
  unsigned __int64 v19; // rcx
  __int64 v20; // r8
  __int64 v21; // r15
  __int64 v23[2]; // [rsp+20h] [rbp-40h] BYREF
  int v24; // [rsp+30h] [rbp-30h] BYREF
  __int64 v25; // [rsp+38h] [rbp-28h] BYREF
  __int64 *v26; // [rsp+48h] [rbp-18h]
  __int64 v27; // [rsp+50h] [rbp-10h]
  unsigned __int64 v28; // [rsp+58h] [rbp-8h]
  __int64 v29; // [rsp+60h] [rbp+0h]

  v29 = -2;
  v2 = a2;
  v27 = a2;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
        v2 = v27;
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  (*(void (__fastcall **)(__int64, int *))(*(_QWORD *)v2 + 144LL))(v2, &v24);
  sub_140FEAD00(&v24, v23);
  sub_140835380(&qword_141B60C30, 1130589301, v23);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v23[0] + 16LL))(v23[0], v23);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
  v4 = *(__int64 ***)(qword_141B601A8 + 128);
  v5 = *v4;
  v6 = v4[1];
  if ( *v4 != v6 )
  {
    v26 = v4[1];
    while ( 1 )
    {
      v7 = *v5;
      v8 = *(_QWORD *)(*v5 + 32);
      if ( v8 == 0 || *(_BYTE *)(v8 + 47) != 0 || *(_QWORD *)(v8 + 48) != v2 )
      {
        v9 = *(_QWORD *)(v7 + 24);
        if ( v9 == 0 || *(_BYTE *)(v9 + 47) != 0 || *(_QWORD *)(v9 + 48) != v2 )
          goto LABEL_7;
      }
      v10 = (_QWORD *)a1[1];
      if ( v10 == (_QWORD *)a1[2] )
        break;
      *v10 = v7;
      a1[1] += 8;
LABEL_7:
      if ( ++v5 == v6 )
        return a1;
    }
    v11 = (__int64)v10 - *a1;
    v12 = v11 >> 3;
    v13 = (unsigned __int64)(v11 >> 3) >> 1;
    v14 = 0x1FFFFFFFFFFFFFFFLL - v13;
    v15 = (v11 >> 3) + v13;
    v28 = (v11 >> 3) + 1;
    if ( v15 <= v28 )
      v15 = v12 + 1;
    if ( v12 > v14 )
      v15 = 0x1FFFFFFFFFFFFFFFLL;
    v16 = sub_1407E4490(qword_141ABD470, 8 * v15);
    *(_QWORD *)(v16 + v11) = v7;
    v17 = (_QWORD *)a1[1];
    sub_141758A00();
    if ( v17 != v10 )
      sub_141758A00();
    v18 = *a1;
    if ( *a1 == 0 )
    {
LABEL_32:
      *a1 = v16;
      a1[1] = v16 + 8 * v28;
      a1[2] = v16 + 8 * v15;
      v2 = v27;
      v6 = v26;
      goto LABEL_7;
    }
    v19 = a1[2] - v18;
    if ( v19 == -1 )
    {
      v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_31:
        MEMORY[0x141948990](v18 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_32;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_31;
    }
    v20 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19 )
    {
      v21 = *(_QWORD *)(v20 + 8 * v19);
      if ( v21 != 0 )
      {
        MEMORY[0x1419475D8](v21 + 32, v18 - *(unsigned int *)(v21 + 120));
        if ( (*(_BYTE *)(v21 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) == 0)
          && *(_BYTE *)(v21 + 97) != 0 )
        {
          sub_1412D33C0(v21);
        }
        goto LABEL_32;
      }
    }
    goto LABEL_31;
  }
  return a1;
}
