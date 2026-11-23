_QWORD *__fastcall sub_1412D5BA0(_QWORD *a1)
{
  __int64 v2; // rsi
  __int64 v3; // rax
  volatile signed __int32 *v4; // rcx
  __int64 v5; // rax
  volatile signed __int32 *v6; // rcx
  volatile signed __int32 **v8; // [rsp+28h] [rbp-8h]

  *a1 = 0x1418964C8LL;
  if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B59AA8);
    if ( dword_141B59AA8 == -1 )
    {
      sub_1407E3E70(&unk_141B59A68);
      sub_141751048(sub_1407E4B20);
      sub_141750EA0(&dword_141B59AA8);
    }
  }
  v2 = sub_1407E4490(&unk_141B59A68, 40);
  *(_DWORD *)v2 = 0;
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
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  *(_DWORD *)(v2 + 32) = 0;
  *(_QWORD *)(v2 + 24) = 0;
  *(_QWORD *)(v2 + 16) = 0;
  *(_QWORD *)(v2 + 8) = 0;
  a1[1] = v2;
  _InterlockedIncrement((volatile signed __int32 *)v2);
  v8 = (volatile signed __int32 **)(a1 + 1);
  if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B59AA8);
    if ( dword_141B59AA8 == -1 )
    {
      sub_1407E3E70(&unk_141B59A68);
      sub_141751048(sub_1407E4B20);
      sub_141750EA0(&dword_141B59AA8);
    }
  }
  v3 = sub_1407E4490(&unk_141B59A68, 32);
  *(_QWORD *)(v3 + 8) = 0;
  *(_DWORD *)(v3 + 16) = 0;
  *(_QWORD *)v3 = 0x141896538LL;
  v4 = *v8;
  *(_QWORD *)(v3 + 24) = *v8;
  if ( v4 != nullptr )
    _InterlockedIncrement(v4);
  a1[2] = v3;
  _InterlockedIncrement((volatile signed __int32 *)(v3 + 8));
  if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B59AA8);
    if ( dword_141B59AA8 == -1 )
    {
      sub_1407E3E70(&unk_141B59A68);
      sub_141751048(sub_1407E4B20);
      sub_141750EA0(&dword_141B59AA8);
    }
  }
  v5 = sub_1407E4490(&unk_141B59A68, 32);
  *(_QWORD *)(v5 + 8) = 0;
  *(_DWORD *)(v5 + 16) = 0;
  *(_QWORD *)v5 = 0x1418965E8LL;
  v6 = *v8;
  *(_QWORD *)(v5 + 24) = *v8;
  if ( v6 != nullptr )
    _InterlockedIncrement(v6);
  a1[3] = v5;
  _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
  return a1;
}
