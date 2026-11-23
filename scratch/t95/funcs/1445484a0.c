__int64 __fastcall sub_1445484A0(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  volatile signed __int32 *v10; // rsi
  _BYTE *v11; // rbx
  __int64 v12; // r9
  __int64 v14; // rdx
  __int64 v15; // rax
  volatile signed __int32 *v16; // rcx
  volatile signed __int32 *v17; // rsi
  volatile signed __int32 *v18; // rdi
  unsigned int *v19; // rbx
  __int64 v20; // r8
  int v21[10]; // [rsp+20h] [rbp-28h] BYREF

  v10 = *a2;
  v11 = (_BYTE *)(a1 + 59);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 59, 1);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_2;
  if ( (*v11 & 1) != 0 )
  {
    sub_140814B10(*a2, v21, a1 + 24);
    if ( v21[0] != 0 )
    {
LABEL_2:
      LODWORD(v10) = 0;
      return (unsigned int)v10;
    }
    v14 = *(_QWORD *)(a1 + 24);
    v15 = *(_QWORD *)(a1 + 32);
    v16 = (volatile signed __int32 *)(v15 - 4);
    if ( v15 == 0 )
      v16 = nullptr;
    v17 = (volatile signed __int32 *)(v14 - 4);
    if ( v14 != 0 )
    {
      if ( v15 != 0 && _InterlockedDecrement(v16) == 0 )
        sub_1412EC9A0(v16, v14);
      *(_QWORD *)(a1 + 32) = 0;
      _InterlockedIncrement(v17);
      v10 = v17 + 1;
    }
    else
    {
      if ( v15 != 0 && _InterlockedDecrement(v16) == 0 )
        sub_1412EC9A0(v16, 0);
      v10 = nullptr;
    }
    *(_QWORD *)(a1 + 32) = v10;
  }
  v18 = *a2;
  if ( v18 != nullptr )
  {
    _InterlockedIncrement(v18 + 2);
    v19 = (unsigned int *)(a1 + 8);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v18 + 40LL))(v18, a1 + 8, 12);
  }
  else
  {
    v19 = (unsigned int *)(a1 + 8);
  }
  v20 = *v19;
  if ( (unsigned int)v20 >= 0x989681 )
  {
    v20 = a6;
    *v19 = a6;
  }
  if ( a8 != 0 )
  {
    LOBYTE(v12) = 1;
    (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, a1, v20, v12);
  }
  LOBYTE(v10) = 1;
  if ( v18 != nullptr && _InterlockedDecrement(v18 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v18)(v18, 1);
  return (unsigned int)v10;
}
