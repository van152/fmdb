bool __fastcall sub_1446580A0(__int64 a1, volatile signed __int32 **a2)
{
  volatile signed __int32 *v3; // r15
  int v4; // ebx
  char v5; // di
  __int64 v6; // r8
  __int64 v7; // rsi
  __int64 v8; // rdx
  int v9; // eax
  __int64 v10; // rax
  __int64 v11; // rsi
  int v12; // esi
  char v14[41]; // [rsp+2Fh] [rbp-29h] BYREF

  v3 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v3 + 2);
    v14[0] = 5;
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v3 + 40LL))(a1: v3, a2: v14, a3: 1);
    v4 = (v14[0] >= 6u) | 0xA;
  }
  else
  {
    v14[0] = 5;
    v4 = 10;
  }
  *(_DWORD *)(a1 + 7) = 0;
  *(_QWORD *)a1 = 0;
  v5 = 1;
  v6 = 0;
  v7 = 0;
  v8 = 0;
  do
  {
    v10 = v7;
    v11 = a1 + (char)(v5 - 1);
    if ( v10 == v11 )
    {
      ++v6;
    }
    else
    {
      if ( v6 != 0 && v3 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, __int64))(*(_QWORD *)v3 + 40LL))(a1: v3, a2: v8);
      v8 = a1 + (char)(v5 - 1);
      v6 = 1;
    }
    v7 = v11 + 1;
    v9 = v5++;
  }
  while ( v4 > v9 );
  if ( v6 != 0 && v3 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, __int64))(*(_QWORD *)v3 + 40LL))(a1: v3, a2: v8);
  v12 = *((_DWORD *)v3 + 4);
  if ( _InterlockedDecrement(v3 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v3)(a1: v3, a2: 1);
  return v12 == 0;
}
