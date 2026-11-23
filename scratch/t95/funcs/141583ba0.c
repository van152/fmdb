__int64 __fastcall sub_141583BA0(
        _QWORD *a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  __int64 v8; // rsi
  volatile signed __int32 *v11; // rbx
  volatile signed __int32 *v12; // rbx
  volatile signed __int32 *v13; // rbx
  __int64 v14; // r9
  __int64 v16; // r14
  volatile signed __int32 *v17; // rbx
  volatile signed __int32 *v18; // rbx
  int v19; // ebp
  volatile signed __int32 *v20; // rbx
  __int64 *v21; // r15
  __int64 v22; // r12
  unsigned __int64 v23; // rax
  unsigned __int64 v24; // rsi
  unsigned __int64 v25; // rcx
  unsigned __int64 v26; // rsi
  __int64 v27; // rbx
  __int64 *v28; // rbp
  __int64 v29; // rbp
  unsigned __int64 v30; // rcx
  __int64 v31; // r8
  __int64 v32; // r14
  bool v33; // al
  volatile signed __int32 *v34; // rdi
  unsigned int *v35; // rbx
  __int64 v36; // r8
  unsigned int v37; // [rsp+40h] [rbp-58h] BYREF
  char v38; // [rsp+47h] [rbp-51h] BYREF
  __int64 v39; // [rsp+48h] [rbp-50h]
  unsigned __int64 v40; // [rsp+50h] [rbp-48h]

  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 6, 4);
  if ( *((_DWORD *)v11 + 4) != 0
    || (v12 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 7, 1),
        *((_DWORD *)v12 + 4) != 0)
    || (v37 = 0,
        v13 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(
          *a2,
          &v37,
          4),
        *((_DWORD *)v13 + 4) != 0) )
  {
LABEL_4:
    LODWORD(v8) = 0;
    return (unsigned int)v8;
  }
  if ( v37 != 0 )
  {
    v8 = 0;
    do
    {
      if ( dword_141B5F758 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5F758);
        if ( dword_141B5F758 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B5F708, 1100140400, 128, 12, 0, 1, 128, 0);
          sub_141751048(sub_140FC6660);
          sub_141750EA0(&dword_141B5F758);
        }
      }
      v16 = sub_1407E58C0(&unk_141B5F708, 12);
      *(_BYTE *)(v16 + 8) = 1;
      *(_QWORD *)v16 = -1;
      v17 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v38, 1);
      if ( *((_DWORD *)v17 + 4) != 0 )
        goto LABEL_4;
      v18 = *a2;
      if ( *a2 != nullptr )
      {
        _InterlockedIncrement(v18 + 2);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v18 + 40LL))(v18, v16, 8);
      }
      if ( *(_DWORD *)(v16 + 4) == 0 )
        *(_DWORD *)(v16 + 4) = *(_DWORD *)v16;
      v19 = *((_DWORD *)v18 + 4);
      if ( _InterlockedDecrement(v18 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v18)(v18, 1);
      if ( v19 != 0 )
        goto LABEL_4;
      v20 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v16 + 8, 1);
      if ( *((_DWORD *)v20 + 4) != 0 || *((_DWORD *)*a2 + 4) != 0 )
        goto LABEL_4;
      v21 = (__int64 *)a1[4];
      if ( v21 == (__int64 *)a1[5] )
      {
        v39 = v8;
        v22 = (__int64)v21 - a1[3];
        v23 = v22 >> 3;
        v24 = (unsigned __int64)(v22 >> 3) >> 1;
        v25 = 0x1FFFFFFFFFFFFFFFLL - v24;
        v26 = (v22 >> 3) + v24;
        v40 = (v22 >> 3) + 1;
        if ( v26 <= v40 )
          v26 = v23 + 1;
        if ( v23 > v25 )
          v26 = 0x1FFFFFFFFFFFFFFFLL;
        v27 = sub_1407E4490(qword_141ABD470, 8 * v26);
        *(_QWORD *)(v27 + v22) = v16;
        v28 = (__int64 *)a1[4];
        sub_141758A00(v27, a1[3], (char *)v21 - a1[3]);
        if ( v28 != v21 )
          sub_141758A00(v27 + v22 + 8, v21, a1[4] - (_QWORD)v21);
        v29 = a1[3];
        if ( v29 != 0 )
        {
          v30 = a1[5] - v29;
          if ( v30 == -1 )
            v30 = *(unsigned int *)(v29 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v31 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v31) >> 3 > v30)
            && (v32 = *(_QWORD *)(v31 + 8 * v30)) != 0 )
          {
            MEMORY[0x1419475D8](v32 + 32, v29 - *(unsigned int *)(v32 + 120));
            v33 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
            if ( !v33 && *(_BYTE *)(v32 + 97) != 0 )
              sub_1412D33C0(v32);
          }
          else
          {
            MEMORY[0x141948990](v29 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        a1[3] = v27;
        a1[4] = v27 + 8 * v40;
        a1[5] = v27 + 8 * v26;
        v8 = v39;
      }
      else
      {
        *v21 = v16;
        a1[4] += 8LL;
      }
    }
    while ( ++v8 < (unsigned __int64)v37 );
  }
  v34 = *a2;
  if ( v34 != nullptr )
  {
    _InterlockedIncrement(v34 + 2);
    v35 = (unsigned int *)(a1 + 1);
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v34 + 40LL))(v34, a1 + 1, 12);
  }
  else
  {
    v35 = (unsigned int *)(a1 + 1);
  }
  v36 = *v35;
  if ( (unsigned int)v36 >= 0x989681 )
  {
    v36 = a6;
    *v35 = a6;
  }
  if ( a8 != 0 )
  {
    LOBYTE(v14) = 1;
    (*(void (__fastcall **)(__int64, _QWORD *, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, a1, v36, v14);
  }
  LOBYTE(v8) = 1;
  if ( v34 != nullptr && _InterlockedDecrement(v34 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v34)(v34, 1);
  return (unsigned int)v8;
}
