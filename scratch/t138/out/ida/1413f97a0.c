char __fastcall sub_1413F97A0(_QWORD *a1, _QWORD *a2)
{
  _QWORD *v2; // rdi
  __int64 v4; // rsi
  int v5; // eax
  __int16 v6; // ax
  __int64 v7; // r13
  __int64 v8; // r15
  __int64 v9; // rbp
  __int64 v10; // r12
  __int64 v11; // rsi
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  int v16; // r13d
  __int64 v17; // r15
  __int64 *v18; // r14
  __int64 v19; // r12
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // rsi
  unsigned __int64 v22; // rcx
  unsigned __int64 v23; // rsi
  __int64 v24; // rbp
  __int64 *v25; // rdi
  __int64 v26; // rdi
  unsigned __int64 v27; // rcx
  __int64 v28; // r8
  __int64 v29; // r14
  __int16 v31; // [rsp+4Eh] [rbp-5Ah] BYREF
  unsigned __int64 v32; // [rsp+50h] [rbp-58h]
  int v33; // [rsp+5Ch] [rbp-4Ch]
  _QWORD *v34; // [rsp+60h] [rbp-48h]

  v2 = a2;
  v31 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v31, a3: 2);
  if ( *(_DWORD *)(v4 + 16) != 0 || (v6 = v31, v31 < 0) )
  {
    LOBYTE(v5) = 0;
  }
  else
  {
    v7 = (unsigned __int16)v31;
    v8 = *a1;
    if ( (__int64)(a1[2] - *a1) >> 3 < (unsigned __int64)(unsigned __int16)v31 )
    {
      v9 = a1[1];
      v10 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (unsigned __int16)v31);
      sub_141758A00(a1: v10, a2: *a1, a3: a1[1] - *a1);
      v11 = *a1;
      if ( *a1 != 0 )
      {
        v32 = (unsigned __int64)a1;
        v12 = a1[2] - v11;
        if ( v12 == -1 )
          v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v13 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12)
          && (v14 = *(_QWORD *)(v13 + 8 * v12)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
          v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
          a1 = (_QWORD *)v32;
          if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
            sub_1412D33C0(a1: v14);
        }
        else
        {
          MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
          a1 = (_QWORD *)v32;
        }
      }
      *a1 = v10;
      a1[1] = v10 + v9 - v8;
      a1[2] = v10 + 8 * v7;
      v6 = v31;
    }
    if ( v6 > 0 )
    {
      v16 = 0;
      v34 = v2;
      while ( 1 )
      {
        if ( dword_141B5CBC0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5CBC0);
          if ( dword_141B5CBC0 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B5CB70,
              a2: 1100154223,
              a3: 4096,
              a4: 40,
              a5: 0,
              a6: 0,
              a7: 512,
              a8: 4096);
            sub_141751048(a1: sub_140DD5990);
            sub_141750EA0(a1: &dword_141B5CBC0);
          }
        }
        v17 = sub_1407E58C0(a1: &unk_141B5CB70, a2: 40);
        *(_QWORD *)v17 = 0;
        *(_QWORD *)(v17 + 8) = 0;
        *(_QWORD *)(v17 + 16) = 0;
        *(_QWORD *)(v17 + 24) = 0;
        *(_DWORD *)(v17 + 32) = 124518401;
        *(_WORD *)(v17 + 36) = 1;
        v5 = sub_1413F94B0(a1: v17, a2: v2);
        if ( (_BYTE)v5 == 0 )
          return v5;
        v18 = (__int64 *)a1[1];
        if ( v18 == (__int64 *)a1[2] )
          break;
        *v18 = v17;
        a1[1] += 8LL;
LABEL_19:
        if ( (__int16)++v16 >= v31 )
          return v5;
      }
      v33 = v5;
      v19 = (__int64)v18 - *a1;
      v20 = v19 >> 3;
      v21 = (unsigned __int64)(v19 >> 3) >> 1;
      v22 = 0x1FFFFFFFFFFFFFFFLL - v21;
      v23 = (v19 >> 3) + v21;
      v32 = (v19 >> 3) + 1;
      if ( v23 <= v32 )
        v23 = v20 + 1;
      if ( v20 > v22 )
        v23 = 0x1FFFFFFFFFFFFFFFLL;
      v24 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v23);
      *(_QWORD *)(v24 + v19) = v17;
      v25 = (__int64 *)a1[1];
      sub_141758A00(a1: v24, a2: *a1, a3: (char *)v18 - *a1);
      if ( v25 != v18 )
        sub_141758A00(a1: v24 + v19 + 8, a2: v18, a3: a1[1] - (_QWORD)v18);
      v26 = *a1;
      if ( *a1 == 0 )
      {
LABEL_40:
        *a1 = v24;
        a1[1] = v24 + 8 * v32;
        a1[2] = v24 + 8 * v23;
        v2 = v34;
        LOBYTE(v5) = v33;
        goto LABEL_19;
      }
      v27 = a1[2] - v26;
      if ( v27 == -1 )
      {
        v27 = *(unsigned int *)(v26 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_39:
          MEMORY[0x141948990](a1: v26 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_40;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_39;
      }
      v28 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v28) >> 3 > v27 )
      {
        v29 = *(_QWORD *)(v28 + 8 * v27);
        if ( v29 != 0 )
        {
          MEMORY[0x1419475D8](a1: v29 + 32, a2: v26 - *(unsigned int *)(v29 + 120));
          if ( (*(_BYTE *)(v29 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) == 0)
            && *(_BYTE *)(v29 + 97) != 0 )
          {
            sub_1412D33C0(a1: v29);
          }
          goto LABEL_40;
        }
      }
      goto LABEL_39;
    }
    LOBYTE(v5) = 1;
  }
  return v5;
}
