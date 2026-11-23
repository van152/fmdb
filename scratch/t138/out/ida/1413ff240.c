__int64 __fastcall sub_1413FF240(__int64 *a1, _QWORD *a2)
{
  unsigned int v2; // r14d
  _QWORD *v5; // rbx
  _QWORD *v6; // rbp
  _QWORD *v7; // rdi
  __int64 v8; // rdi
  __int64 v9; // rdi
  unsigned __int64 v11; // rbp
  _QWORD *v12; // r15
  __int64 v13; // rdi
  __int64 v14; // rbx
  __int64 v15; // rdi
  __int64 v16; // rdi
  __int64 v17; // rdi
  __int64 v18; // rdi
  __int64 *v19; // rsi
  _QWORD *v20; // r13
  unsigned __int64 v21; // rbp
  __int64 v22; // rbp
  unsigned __int64 v23; // rbx
  unsigned __int64 v24; // rax
  unsigned __int64 v25; // rcx
  unsigned __int64 v26; // rax
  __int64 v27; // rdi
  __int64 v28; // rbx
  _QWORD *v29; // r15
  __int64 v30; // r15
  __int64 v31; // rbx
  unsigned __int64 v32; // rcx
  __int64 v33; // r8
  __int64 v34; // rcx
  __int64 v35; // rbx
  __int64 v36; // rcx
  bool v37; // al
  unsigned __int8 v38; // [rsp+42h] [rbp-66h] BYREF
  char v39; // [rsp+43h] [rbp-65h] BYREF
  unsigned int v40; // [rsp+44h] [rbp-64h] BYREF
  __int64 v41; // [rsp+48h] [rbp-60h]
  unsigned __int64 v42; // [rsp+50h] [rbp-58h]
  unsigned __int64 v43; // [rsp+58h] [rbp-50h]
  __int64 *v44; // [rsp+60h] [rbp-48h]

  v5 = (_QWORD *)*a1;
  v6 = (_QWORD *)a1[1];
  if ( (_QWORD *)*a1 != v6 )
  {
    v7 = (_QWORD *)*a1;
    do
    {
      if ( *v7 != 0 )
        sub_140DD51D0();
      ++v7;
    }
    while ( v7 != v6 );
    v8 = a1[1] - (_QWORD)v6;
    sub_141758A00(a1: v5, a2: v6, a3: v8);
    a1[1] = (__int64)v5 + v8;
  }
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v40, a3: 4);
  if ( *(_DWORD *)(v9 + 16) == 0 )
  {
    if ( v40 == 0 )
    {
      LOBYTE(v2) = 1;
      return v2;
    }
    v11 = 0;
    v44 = a1;
    while ( 1 )
    {
      if ( dword_141B5CC18 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5CC18);
        if ( dword_141B5CC18 == -1 )
        {
          sub_1407E53D0(a1: (unsigned int)&unk_141B5CBC8, a2: 1100126260, a3: 256, a4: 56, a5: 0, a6: 0, a7: 256, a8: 0);
          sub_141751048(a1: sub_140DD5340);
          sub_141750EA0(a1: &dword_141B5CC18);
        }
      }
      v12 = (_QWORD *)sub_1407E58C0(a1: &unk_141B5CBC8, a2: 56);
      v12[6] = -1;
      *v12 = 0;
      v12[1] = 0;
      v12[2] = 0;
      v12[3] = 0;
      v12[4] = 0;
      *(_QWORD *)((char *)v12 + 39) = 0;
      v13 = *a2;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v38, a3: 1);
      if ( *(_DWORD *)(v13 + 16) != 0 )
        return 0;
      v14 = 0;
      if ( v38 <= 1u )
      {
        do
        {
          v16 = *a2;
          (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v39, a3: 1);
          if ( *(_DWORD *)(v16 + 16) != 0 )
            return 0;
          *((_BYTE *)v12 + v14++) = v39;
        }
        while ( v14 != 47 );
        goto LABEL_24;
      }
      if ( v38 <= 2u )
        break;
      while ( 1 )
      {
LABEL_18:
        v15 = *a2;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (char *)v12 + v14, a3: 1);
        if ( *(_DWORD *)(v15 + 16) != 0 )
          return 0;
LABEL_19:
        if ( v14 == 46 )
          break;
        ++v14;
        if ( v38 <= 2u )
          goto LABEL_16;
      }
LABEL_24:
      v17 = *a2;
      (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v12 + 6, a3: 4);
      if ( *(_DWORD *)(v17 + 16) != 0 )
        return 0;
      v18 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)v12 + 52, a3: 4);
      LOBYTE(v2) = *(_DWORD *)(v18 + 16) == 0;
      if ( *(_DWORD *)(v18 + 16) == 0 )
      {
        v42 = v11;
        v19 = v44;
        v20 = (_QWORD *)v44[1];
        if ( v20 == (_QWORD *)v44[2] )
        {
          v22 = (__int64)v20 - *v44;
          v23 = v22 >> 3;
          v24 = (unsigned __int64)(v22 >> 3) >> 1;
          v25 = 0x1FFFFFFFFFFFFFFFLL - v24;
          v26 = (v22 >> 3) + v24;
          v43 = (v22 >> 3) + 1;
          if ( v26 <= v43 )
            v26 = v23 + 1;
          v27 = v26;
          if ( v23 > v25 )
            v27 = 0x1FFFFFFFFFFFFFFFLL;
          v28 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v27);
          *(_QWORD *)(v28 + v22) = v12;
          v29 = (_QWORD *)v19[1];
          sub_141758A00(a1: v28, a2: *v19, a3: (char *)v20 - *v19);
          if ( v29 != v20 )
            sub_141758A00(a1: v28 + v22 + 8, a2: v20, a3: v19[1] - (_QWORD)v20);
          v30 = v28;
          v31 = *v19;
          v21 = v42;
          if ( *v19 != 0 )
          {
            v32 = v19[2] - v31;
            if ( v32 == -1 )
              v32 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v33 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 > v32)
              && (v34 = *(_QWORD *)(v33 + 8 * v32)) != 0 )
            {
              v35 = v31 - *(unsigned int *)(v34 + 120);
              v41 = v34;
              MEMORY[0x1419475D8](a1: v34 + 32, a2: v35);
              v36 = v41;
              v37 = *(_BYTE *)(v41 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v41 + 64)) != 0;
              if ( !v37 && *(_BYTE *)(v36 + 97) != 0 )
                sub_1412D33C0(a1: v36);
            }
            else
            {
              MEMORY[0x141948990](a1: v31 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *v19 = v30;
          v19[1] = v30 + 8 * v43;
          v19[2] = v30 + 8 * v27;
        }
        else
        {
          *v20 = v12;
          v19[1] += 8;
          v21 = v42;
        }
        v11 = v21 + 1;
        if ( v11 < v40 )
          continue;
      }
      return v2;
    }
LABEL_16:
    if ( (unsigned int)(unsigned __int8)v14 - 33 < 7 || (unsigned __int8)v14 == 11 )
      goto LABEL_19;
    goto LABEL_18;
  }
  return 0;
}
