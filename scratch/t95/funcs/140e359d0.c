__int64 __fastcall sub_140E359D0(_QWORD **a1)
{
  _QWORD *v1; // rdi
  _QWORD *v2; // r14
  _QWORD *v3; // rsi
  _QWORD *v4; // rbx
  __int64 v5; // rbx
  __int64 result; // rax
  __int64 v7; // rsi
  __int64 *v8; // rdi
  void (__fastcall *v9)(__int64); // r14
  void (__fastcall *v10)(__int64); // r15
  __int64 v11; // rcx

  v1 = *a1;
  if ( *a1 != nullptr )
  {
    v2 = (_QWORD *)*v1;
    v3 = (_QWORD *)v1[1];
    if ( (_QWORD *)*v1 != v3 )
    {
      v4 = (_QWORD *)*v1;
      do
      {
        if ( *v4 != 0 )
          (**(void (__fastcall ***)(_QWORD, __int64))*v4)(*v4, 1);
        ++v4;
      }
      while ( v4 != v3 );
      v5 = v1[1] - (_QWORD)v3;
      sub_141758A00();
      v1[1] = (char *)v2 + v5;
      v3 = (_QWORD *)*v1;
    }
    if ( v3 != nullptr )
    {
      sub_1407E6420(qword_141ABE200, v3, v1[2] - (_QWORD)v3);
      v1[2] = 0;
      v1[1] = 0;
      *v1 = 0;
    }
    if ( dword_141ABEC98 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141ABEC98);
      if ( dword_141ABEC98 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141ABEC48, 1100123278, 128, 24, 0, 0, 128, 4096);
        sub_141751048(sub_1400D9390);
        sub_141750EA0(&dword_141ABEC98);
      }
    }
    result = qword_141ABEC70;
    *v1 = qword_141ABEC70;
    qword_141ABEC70 = (__int64)v1;
    LODWORD(qword_141ABEC78) = qword_141ABEC78 + 1;
    if ( --HIDWORD(qword_141ABEC78) == 0 && byte_141ABEC91 != 0 )
    {
      v7 = qword_141ABEC60;
      v8 = (__int64 *)qword_141ABEC58;
      if ( qword_141ABEC58 != qword_141ABEC60 )
      {
        v9 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v10 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v11 = *v8;
          if ( (dword_141ABEC50 & 0xFFF000u) < 0x2001 )
            v10(v11);
          else
            v9(v11);
          ++v8;
        }
        while ( v8 != (__int64 *)v7 );
        result = qword_141ABEC58;
        if ( qword_141ABEC58 != qword_141ABEC60 )
          qword_141ABEC60 = qword_141ABEC58;
      }
      qword_141ABEC78 = 0;
      qword_141ABEC70 = 0;
    }
  }
  return result;
}
