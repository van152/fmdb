bool __fastcall sub_143F2B820(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        _QWORD *a8)
{
  volatile signed __int32 *v11; // rbx
  __int64 v12; // r9
  int v13; // ebp
  volatile signed __int32 *v15; // rbx
  unsigned int *v16; // rdi
  unsigned int v17; // r12d
  _QWORD *v18; // rdx
  __int64 v19; // rbx

  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(
    a1: v11,
    a2: a1 + 24,
    a3: 8);
  v13 = *((_DWORD *)v11 + 4);
  if ( v13 == 0 )
  {
    v15 = *a2;
    if ( *a2 != nullptr )
    {
      _InterlockedIncrement(v15 + 2);
      v16 = (unsigned int *)(a1 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
        a1: v15,
        a2: a1 + 8,
        a3: 12);
    }
    else
    {
      v16 = (unsigned int *)(a1 + 8);
    }
    v17 = a6;
    if ( *v16 >= 0x989681 )
      *v16 = a6;
    if ( v15 != nullptr && _InterlockedDecrement(v15 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v15)(a1: v15, a2: 1);
    if ( (a6 & 0x80000000) == 0 )
    {
      *(_DWORD *)(a1 + 8) = a6;
      if ( *(_QWORD **)(a4 + 104) != a8 || (_BYTE)word_141B60320 == 0 )
      {
        LOBYTE(v12) = 1;
        (*(void (__fastcall **)(_QWORD *, __int64, _QWORD, __int64))(*a8 + 24LL))(a1: a8, a2: a1, a3: a6, a4: v12);
        return v13 == 0;
      }
      v18 = (_QWORD *)a8[16];
      if ( (__int64)(v18[1] - *v18) >> 3 > (unsigned __int64)a6 )
      {
        v19 = *(_QWORD *)(*v18 + 8LL * a6);
        if ( v19 != 0 )
        {
          if ( (*(_BYTE *)(v19 + 26) & 0x40) == 0 )
            goto LABEL_19;
          sub_140F90D90(a1: &qword_141B5FDA8, a2: v19);
          v17 = *(_DWORD *)(a1 + 8);
        }
      }
      v19 = 0;
LABEL_19:
      (*(void (__fastcall **)(_QWORD *, __int64, _QWORD, _QWORD))(*a8 + 24LL))(a1: a8, a2: a1, a3: v17, a4: 0);
      if ( v19 != 0 )
        (**(void (__fastcall ***)(__int64, __int64))v19)(a1: v19, a2: 1);
    }
  }
  return v13 == 0;
}
