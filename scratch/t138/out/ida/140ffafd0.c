_DWORD *__fastcall sub_140FFAFD0(_DWORD *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // rbx
  __int64 v6; // rbp
  __int64 v7; // r15
  unsigned __int64 v8; // rax
  __int64 *v9; // rdi
  __int64 v10; // r13
  __int64 v11; // r12
  __int64 v12; // rsi
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // r14
  bool v16; // al
  __int64 v17; // r14
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rbp
  __int64 v22; // r15
  unsigned __int64 v23; // rax
  unsigned __int64 v24; // r12
  unsigned __int64 v25; // rbx
  __int64 v26; // rsi
  __int64 v27; // rdx
  __int64 v28; // r13
  bool v29; // zf
  __int64 v30; // rbp
  unsigned __int64 v31; // rcx
  __int64 v32; // r8
  __int64 v33; // r15
  unsigned int v35; // [rsp+2Ch] [rbp-6Ch] BYREF
  __int64 v36; // [rsp+30h] [rbp-68h] BYREF
  int v37; // [rsp+38h] [rbp-60h] BYREF
  __int64 *v38; // [rsp+40h] [rbp-58h]
  _DWORD *v39; // [rsp+48h] [rbp-50h]
  _QWORD *v40; // [rsp+50h] [rbp-48h]

  v4 = a2;
  v35 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v35, a3: 4);
  v6 = v35;
  if ( qword_141AA7808 <= (unsigned __int64)v35 )
  {
LABEL_44:
    *a1 = 1;
    return a1;
  }
  v39 = a1;
  v7 = *a3;
  v8 = 0xAAAAAAAAAAAAAAABuLL * ((a3[2] - *a3) >> 2);
  v38 = a3;
  if ( v8 < v35 )
  {
    v9 = a3;
    v10 = a3[1];
    v11 = sub_1407E4490(a1: qword_141ABD470, a2: 12LL * v35);
    sub_141758A00(a1: v11, a2: *v9, a3: v9[1] - *v9);
    v12 = *v9;
    if ( *v9 == 0 )
    {
LABEL_13:
      *v9 = v11;
      v9[1] = v11 + v10 - v7;
      v9[2] = v11 + 12 * v6;
      LODWORD(v6) = v35;
      a3 = v9;
      goto LABEL_14;
    }
    v13 = v9[2] - v12;
    if ( v13 == -1 )
    {
      v13 = *(unsigned int *)(v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](a1: v12 - *(unsigned int *)(qword_141ABD470 + 48));
        v9 = v38;
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v13);
      if ( v15 != 0 )
      {
        MEMORY[0x1419475D8](a1: v15 + 32, a2: v12 - *(unsigned int *)(v15 + 120));
        v16 = *(_BYTE *)(v15 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) != 0;
        v9 = v38;
        if ( !v16 && *(_BYTE *)(v15 + 97) != 0 )
          sub_1412D33C0(a1: v15);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  if ( (_DWORD)v6 != 0 )
  {
    v17 = 0;
    v40 = v4;
    while ( 1 )
    {
      v37 = 0;
      v36 = 0;
      v18 = *v4;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v36, a3: 4);
      if ( *(_DWORD *)(v18 + 16) != 0
        || (v19 = *v4,
            (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v4 + 40LL))(
              a1: *v4,
              a2: (char *)&v36 + 4,
              a3: 4),
            *(_DWORD *)(v19 + 16) != 0)
        || (v20 = *v4,
            (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v37, a3: 4),
            *(_DWORD *)(v20 + 16) != 0)
        || *(_DWORD *)(*v4 + 16LL) != 0 )
      {
        a1 = v39;
        goto LABEL_44;
      }
      v21 = a3[1];
      if ( v21 == a3[2] )
        break;
      *(_DWORD *)(v21 + 8) = v37;
      *(_QWORD *)v21 = v36;
      a3[1] += 12;
LABEL_17:
      if ( ++v17 >= (unsigned __int64)v35 )
        goto LABEL_45;
    }
    v22 = v21 - *a3;
    v23 = 0xAAAAAAAAAAAAAAABuLL * (v22 >> 2);
    v24 = v23 + (v23 >> 1);
    v25 = v23 + 1;
    if ( v24 <= v23 + 1 )
      v24 = v23 + 1;
    if ( v23 > 0x1555555555555555LL - (v23 >> 1) )
      v24 = 0x1555555555555555LL;
    v26 = sub_1407E4490(a1: qword_141ABD470, a2: 12 * v24);
    *(_QWORD *)(v26 + v22) = v36;
    *(_DWORD *)(v26 + v22 + 8) = v37;
    v27 = *a3;
    v28 = v38[1];
    sub_141758A00(a1: v26, a2: v27, a3: v21 - v27);
    v29 = v28 == v21;
    a3 = v38;
    if ( !v29 )
      sub_141758A00(a1: v26 + v22 + 12, a2: v21, a3: v38[1] - v21);
    v30 = *a3;
    if ( *a3 == 0 )
    {
LABEL_40:
      *a3 = v26;
      a3[1] = v26 + 12 * v25;
      a3[2] = v26 + 12 * v24;
      v4 = v40;
      goto LABEL_17;
    }
    v31 = a3[2] - v30;
    if ( v31 == -1 )
    {
      v31 = *(unsigned int *)(v30 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_39:
        MEMORY[0x141948990](a1: v30 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_40;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_39;
    }
    v32 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v32) >> 3 > v31 )
    {
      v33 = *(_QWORD *)(v32 + 8 * v31);
      if ( v33 != 0 )
      {
        MEMORY[0x1419475D8](a1: v33 + 32, a2: v30 - *(unsigned int *)(v33 + 120));
        if ( (*(_BYTE *)(v33 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v33 + 64)) == 0)
          && *(_BYTE *)(v33 + 97) != 0 )
        {
          sub_1412D33C0(a1: v33);
        }
        goto LABEL_40;
      }
    }
    goto LABEL_39;
  }
LABEL_45:
  a1 = v39;
  *v39 = *(_DWORD *)(*v4 + 16LL);
  return a1;
}
